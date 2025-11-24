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

# ────────────────────────────────────────
# 🍇 file load & cache
# ────────────────────────────────────────
# document 전체 HTML 을 가진 Beautiful soup object 값이 전달된다
# 여기서 검색(search) 하거나, HTML element 들을 제거할수 있다.
# 이 함수는 Document 에 포함하고 싶은 text 를 리턴해야 한다
def parse_page(soup):
    header = soup.select_one("#header")  # id='header' 인 element 
    footer = soup.select_one("#footer")  # id='footer' 인 element
    
    # decompose() 해당 element 를 HTML 문서에서 제거
    if header:
        header.decompose()
    
    if footer:
        footer.decompose()
    
    # 전체 페이지에서 header 와 footer 를 제거한 나머지 text 를 리턴한다.
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
        # load 하고 싶은 url 들을 담은 list, 이때 url 은 정규표현식으로 다루어짐.
        filter_urls=[
            # "https://mistral.ai/news/ai-studio",  # 특정 뉴스 페이지 url 하나를 보자.

            # 정규표현식 사용
            # .*  ← 전 후에 다른 문자들이 올수는 있지만
            #  /news/ 를 포함하는 url 만 볼수 있다.
            r"^(.*\/news\/).*",              

            # ?! ← negative lookahead   /news/ 롤 포함하지 않은 url만 통과
            # r"^(?!.*\/news\/).*",              
        ],
        parsing_function=parse_page,
    )
    loader.max_depth = 1    # 기본값 10
    loader.headers = {'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Mobile Safari/537.36'}
    docs = loader.load_and_split(text_splitter=splitter)
    return docs


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
        docs = load_website(url)
        st.write(docs) # 확인용.
