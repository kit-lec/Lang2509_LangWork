import os, time
from dotenv import load_dotenv

load_dotenv()  #

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...') # OPENAI_API_KEY 필요!
#─────────────────────────────────────────────────────────────────────────────────────────
import streamlit as st
import glob

from langchain_openai.chat_models.base import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_community.document_loaders.text import TextLoader
from langchain_text_splitters.character import RecursiveCharacterTextSplitter
from langchain_core.output_parsers import StrOutputParser

from langchain_community.vectorstores.faiss import FAISS
from langchain.embeddings.cache import CacheBackedEmbeddings
from langchain_openai.embeddings.base import OpenAIEmbeddings
from langchain.storage.file_system import LocalFileStore

import subprocess
import math
from pydub import AudioSegment
import openai




# ────────────────────────────────────────
# 🎃 LLM 로직
# ────────────────────────────────────────
llm = ChatOpenAI(
    temperature=0.1,
)



# ────────────────────────────────────────
# 🍇 file load & cache
# ────────────────────────────────────────
file_dir = os.path.dirname(os.path.realpath(__file__)) # *.py 파일의 '경로'만
# .cache  ← 업로드한 비디오 와 변환한 mp3
# .cache/chunks ← 분할된 mp3 파일들 저장
upload_dir = os.path.join(file_dir, '.cache/chunks')
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir)


# 오디오 추출함수
# 업로드한 video(mp4)에서 오디오(mp3) 추출하여 동일 경로에 저장.
@st.cache_resource()
def extract_audio_from_video(video_path):    
    audio_path = video_path.replace("mp4", "mp3")  
    command = [
        "ffmpeg",
        "-i",
        video_path,
        "-vn",
        audio_path,
        "-y",  # -y 옵션이 있어야 yes / no 물어볼시 yes 자동선택하고 넘어가게 된다.
        ]
    subprocess.run(command)



# ────────────────────────────────────────
# ⭕ Streamlit 로직
# ────────────────────────────────────────
st.set_page_config(
    page_title="MeetingGPT",
    page_icon="🎤",
)
st.markdown(
    """
# MeetingGPT
            
Welcome to MeetingGPT, upload a video and I will give you a transcript, a summary and a chat bot to ask any questions about it.

Get started by uploading a video file in the sidebar.
"""
)

with st.sidebar:
    video = st.file_uploader(
        label="Video",
        type=["mp4", "avi", "mkv", "mov"],
    )

    if video:
        video_content = video.read()
        video_path = os.path.join(file_dir, rf'.cache/{video.name}')
        with open(video_path, 'wb') as f:
            f.write(video_content)

        extract_audio_from_video(video_path)

