import streamlit as st
import os
import time

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력

st.title('좋은아침 streamlit')
st.text(time.strftime('%Y년%m월%d일 %H:%M:%S'))

# 실행
# streamlit run 파일명