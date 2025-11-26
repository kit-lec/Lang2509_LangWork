import os, time
from dotenv import load_dotenv

load_dotenv()

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...') # OPENAI_API_KEY 필요!
#─────────────────────────────────────────────────────────────────────────────────────────
import streamlit as st

from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain_core.runnables.passthrough import RunnablePassthrough
from langchain_core.runnables.base import RunnableLambda
from langchain_openai.chat_models.base import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate

from langchain_community.document_loaders.sitemap import SitemapLoader


# ────────────────────────────────────────
# 🎃 LLM 로직
# ────────────────────────────────────────
llm = ChatOpenAI(
    temperature=0.1,
)

answers_prompt = ChatPromptTemplate.from_template("""
    Using ONLY the following context answer the user's question. If you can't just say you don't know, don't make anything up.
                                                 
    Then, give a score to the answer between 0 and 5.

    If the answer answers the user question the score should be high, else it should be low.

    Make sure to always include the answer's score even if it's 0.

    Context: {context}
                                                 
    Examples:
                                                 
    Question: How far away is the moon?
    Answer: The moon is 384,400 km away.
    Score: 5
                                                 
    Question: How far away is the sun?
    Answer: I don't know
    Score: 0
                                                 
    Your turn!

    Question: {question}
""")

choose_prompt = ChatPromptTemplate.from_messages([
    ('system', '''
            Use ONLY the following pre-existing answers to answer the user's question.

            Use the answers that have the highest score (more helpful) and favor the most recent ones.

            Cite sources and return the sources as it is. Do not change them. Keep it as a link

            Answers: {answers}
     '''),
    ("human", "{question}"),
])


def get_answers(inputs):
    docs = inputs['docs']
    question = inputs['question']

    # 위 모든 documente 를 처리해줄 chain 
    answers_chain = answers_prompt | llm


    # 다음과 같은 형식으로 리턴해볼거다
    # {
    #     answer: from the llm,
    #     source: doc.metadata   <- Document 의 meta data 포함
    #     date: doc.lastmod  <- Document 의 마지막 수정날짜 정보도 필요.
    # }

    return {
        "question": question,
        "answers": [
            {
                "answer": answers_chain.invoke({
                                "question": question,
                                "context": doc.page_content,
                            }).content,
                "source": doc.metadata['source'],
                "date": doc.metadata['lastmod'],
            }
            
            for doc in docs
        ]
    }

# 입력은 '모든 answer' 와  '사용자 question'
# 출력은 선택된 '최종 answer'.
def choose_answer(inputs):
    answers = inputs['answers']
    question = inputs['question']
    choose_chain = choose_prompt | llm

    # answers 가 dict 의 list 다. 이를 string 으로 만들어 chain 호출하자.
    condensed = "\n\n".join(
        f"{answer['answer']}\nSource:{answer['source']}\nDate:{answer['date']}\n"
        for answer in answers
    )

    return choose_chain.invoke({
        "question": question,
        "answers": condensed,
    })

# ────────────────────────────────────────
# 🍇 file load & cache
# ────────────────────────────────────────
def parse_page(soup):
    header = soup.select_one("#header")  # id='header' 인 element 
    footer = soup.select_one("#footer")  # id='footer' 인 element
    
    if header:
        header.decompose()
    
    if footer:
        footer.decompose()
    
    return (
        str(soup.get_text())
        .replace('\n', " ")  # 줄바꿈 문자
        .replace('\xa0', " ") # &nbsp; 문자
        .replace('The next chapter of AI is yours.', '')
        )

@st.cache_resource(show_spinner="Fetching URL...")
def load_website(url):

    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000,
        chunk_overlap=200,
    )


    loader = SitemapLoader(
        url,
        # filter_urls=[
        #     r"^(.*\/news\/).*",              
        # ],
        parsing_function=parse_page,
    )
    loader.max_depth = 1    # 기본값 10
    loader.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36'}
    docs = loader.load_and_split(text_splitter=splitter)

    vector_store = FAISS.from_documents(
        documents=docs,
        embedding=OpenAIEmbeddings(),
    )

    return vector_store.as_retriever()


# ────────────────────────────────────────
# ⭕ Streamlit 로직
# ────────────────────────────────────────
st.set_page_config(
    page_title="SiteGPT",
    page_icon="🖥️",
)

st.markdown(
"""
    # SiteGPT
            
    Ask questions about the content of a website.
            
    Start by writing the URL of the website on the sidebar.
"""
)

with st.sidebar:
    url = st.text_input(
        "Write down a URL",
        placeholder="https://example.com",
    )

if url:
    # URL 에 XML sitemap 이 포함되는지 확인하자.
    if ".xml" not in url:
        with st.sidebar:
            st.error("Please write down a sitemap URL")
    else:
        retriever = load_website(url)
        query = st.text_input("Ask a question to the website.")

        # Map Re-Rank Chain 만들기. 두개의 chain 이 필요하다
        # 1.첫번째 chain
        #   모든 개별 Document 에 대한 답변 생성 및 채점 담당
        # 2.두번째 chain
        #   모든 답변을 가진 마지막 시점에 실행된다
        #   점수가 제일 높고 + 가장 최신 정보를 담고 있는 답변들 고른다
        if query:
            chain = {
                "docs": retriever,
                "question": RunnablePassthrough(),
            } | RunnableLambda(get_answers) | RunnableLambda(choose_answer)

            result = chain.invoke(query)
            st.markdown(result.content)









