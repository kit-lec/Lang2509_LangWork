import os
import time
from dotenv import load_dotenv

load_dotenv()

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...') # OPENAI_API_KEY 필요!
#─────────────────────────────────────────────────────────────────────────────────────────

import streamlit as st

from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain_text_splitters.character import CharacterTextSplitter

from langchain_openai.chat_models.base import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from langchain_community.retrievers.wikipedia import WikipediaRetriever


# ────────────────────────────────────────
# 🎃 LLM 로직
# ────────────────────────────────────────



# ────────────────────────────────────────
# 🍇 file load & cache
# ────────────────────────────────────────



# ────────────────────────────────────────
# ⭕ Streamlit 로직
# ────────────────────────────────────────
st.set_page_config(
    page_title="QuizGPT",
    page_icon="👩‍🚒",
)

st.title("QuizGPT")

with st.sidebar:
    docs = None  # 읽어들인 문서들 List[Document]
    
    choice = st.selectbox(
        label="Choose what you want to use",
        options=(
            "File",
            "Wikipedia Article",
        ),
    )

    if choice == "File":
        file = st.file_uploader(
            "Upload a .docx , .txt or .pdf file",
            type=["pdf", "txt", "docx"],            
        )
        # TODO: 파일업로드 처리 구현

    else:
        topic = st.text_input("Search Wikipedia...")
        # Wikipedia Retriever 검색기 사용.
        if topic:
            retriever = WikipediaRetriever()

            with st.status("Searching Wikipedia..."):
                docs = retriever.invoke(topic)
                st.write(len(docs), '개의 문서 retrieve') # 확인용
                st.write(docs)  # 확인용





























