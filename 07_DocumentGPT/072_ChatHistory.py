import os
import time

from langchain_community.document_loaders.unstructured import UnstructuredFileLoader
from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain.storage.file_system import LocalFileStore
from langchain_text_splitters.character import CharacterTextSplitter
from langchain_community.vectorstores.faiss import FAISS

from dotenv import load_dotenv
load_dotenv()

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}') # 실행파일명, 현재시간출력

print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...') # OPENAI_API_KEY 필요!

import streamlit as st

st.set_page_config(
    page_title="DocumentGPT",
    page_icon="📃",
)

# ────────────────────────────────────────
# 🍇 file load & cache
# ────────────────────────────────────────

upload_dir = r'./.cache/files'
embedding_dir = r'./.cache/embeddings'

if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)
if not os.path.exists(embedding_dir):
    os.makedirs(embedding_dir)

# @st.cache_resource
# def embed_file(file매개변수) 
#   https://docs.streamlit.io/develop/api-reference/caching-and-state/st.cache_resource
#   최초 embed_file(file) 호출시 실행될것이다.  그리고 리턴값을 cache 해둔다.
#   그러나 두번째 호출시에는 만약 이 매개변수 file 이 동일하다면  
#                          (즉 유저가 다른 파일을 올리지 않았다면)
#   Streamlit 은 이 함수의 호출을 재실행하지 않는다.
#   대신에! 기존에 리턴했던 cache 되었던 값을 다시 리턴된다!

#   show_spinner= 옵션
#     혹시 기존에 cache 된것이 없으면 cache 데이터가 생성되는 동안 spinner UI 동작 
#     True 혹은 특정 문자열 "Embedding file..." 로 설정해줄수 있다.

#  embed_file(file) <- streamlit 은 매개변수 file 에 대해 hash 해 두었다가
#                     재호출시 매개변수 file 이 변경되었다는 사실을 알아챈다

@st.cache_resource(show_spinner="Embedding file...")
def embed_file(file):
    file_content = file.read()
    file_path = os.path.join(upload_dir, file.name)

    with open(file_path, 'wb') as f:
        f.write(file_content)
    
    cache_dir = LocalFileStore(os.path.join(embedding_dir, file.name))

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )

    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)

    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

    vectorstore = FAISS.from_documents(docs, cached_embeddings)

    retriever = vectorstore.as_retriever()
    return retriever

# ────────────────────────────────────────
# ⭕ Streamlit 로직
# ────────────────────────────────────────

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        st.session_state['messages'].append({'message': message, 'role': role})

def paint_history():
    for message in st.session_state['messages']:
        send_message(message['message'], message['role'], save=False)

st.title("Document GPT")

st.markdown("""
안녕하세요!
이 챗봇을 사용해서 여러분의 파일들에 대해 AI에 물어보세요
""")

file = st.file_uploader(
    label="Upload a .txt .pdf or .docx file",
    type=['pdf', 'txt', 'docx']
)

if file:
    retriever = embed_file(file)

    send_message('준비되었습니다. 질문해보세요!', 'ai', save=False)
    paint_history()
    message = st.chat_input('업로드한 file 에 대해 질문을 남겨보세요...')
    if message:
        send_message(message, 'human')
        send_message('어쩌구 저쩌구', 'ai')


else:
    st.session_state['messages'] = [] 