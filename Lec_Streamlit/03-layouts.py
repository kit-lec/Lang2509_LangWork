import streamlit as st
import os
import time

import numpy as np

from dotenv import load_dotenv
load_dotenv()


print(f'✅ {os.path.basename(__file__)} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...')

st.title('layout')

# layout
#  streamlit 에서 제공하는 다양한 레이아웃 
#  공식: https://docs.streamlit.io/develop/api-reference/layout  (◀ 함 보자!)


# container vs. empty

# 레이아웃 사용방식
# 방식1
cont = st.container(border=True)
cont.write('container 내부의 element')
cont.markdown('container 내부의 markdown')

st.write('container 바깥의 요소')
cont.write('이건 어데로?')

# 방식2 (추천) with 사용
with st.container(border=True):
    # with 블럭 안에서 st. 으로 호출하는 모든 요소는 container 안에 그려진다.
    st.write('컨테이너 안 입니다')    
    st.bar_chart(np.random.randn(50, 3))

# container() : 여러 요소들을 담는다
# empty() : 한개의 요소만 담는다.

with st.empty():
    st.write('고양이')
    st.write("강아지")  # 오직 한개의 요소만 그려진다!













