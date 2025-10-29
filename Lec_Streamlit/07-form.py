import streamlit as st

import os
import time

from dotenv import load_dotenv
load_dotenv()

print(f'✅ {os.path.basename(__file__)} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...')


st.title('form')

st.header('1. 커피 머신')

with st.form(key='my_form'): # key=  form식별자.
    st.subheader('**커피 주문하기**')

    # 입력 위젯
    coffee_bean_val = st.selectbox('커피콩', ['아라비카', '로브스타'])
    coffee_roast_val = st.selectbox('커피 로스팅', ['라이트', '미디엄', '다크'])
    brewing_val = st.selectbox('추출 방법', ['에어로프레스', '드립', '프렌치 프레스', '모카 포트', '사이폰'])
    serving_type_val = st.selectbox('서빙 형식', ['핫', '아이스', '프라페'])
    milk_val = st.select_slider('우유 정도', ['없음', '낮음', '중간', '높음'])
    owncup_val = st.checkbox('자신의 컵 가져오기')

    # 모든 form 은 제출버튼이 있어야 함.
    submitted = st.form_submit_button('제출')

if submitted:
    st.markdown(f'''
        ☕ 주문하신 내용:
        - 커피콩: `{coffee_bean_val}`
        - 커피 로스팅: `{coffee_roast_val}`
        - 추출 방법: `{brewing_val}`
        - 서빙 형식: `{serving_type_val}`
        - 우유: `{milk_val}`
        - 자신의 컵 가져오기: `{owncup_val}`
        ''') 
else:
    st.write('☝️ 주문하세요!')   

















