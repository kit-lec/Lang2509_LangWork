# 학습목표:
# Streamlit 의 data flow 와 data 가 처리되는 방식

# Streamlit 에선 'data 가 변경'될때 마다 python 파일 '전체'가 다시 실행된다. (py 파일 위에서부터 아래까지 전부 다시 실행)
# 가령 사용자가 무언가를 입력하거나 slider 를 드래그 해서 data 가 변경될때마다 ..

import streamlit as st
import numpy as np
import pandas as pd

import os
import time

from dotenv import load_dotenv
load_dotenv()

print(f'✅ {os.path.basename(__file__)} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...')

# 다양한 입력 widgets 들
#    https://docs.streamlit.io/develop/api-reference/widgets

st.title(time.strftime('%Y-%m-%d %H:%M:%S'))

model = st.selectbox("Choose your model", ("GPT-3", "GPT-4"))
st.markdown(f'model: :green[{model}]')

name = st.text_input("What is your name?")
st.markdown(f'name: :green[{name}]')

# ↑ 위 input 에서 입력하고 엔터 눌러보자!
#  화면의 모든것이 refresh 된다 (시간을 보면 알수 있다.)
#  ※ 타이핑할때 변경되는 것이 아니다.

# 여기서 'refresh' 된다는 것은 브라우저 좌상단의 reload 의 의미는 아니다.
# refresh 는 py 파일 전체가 위에서부터 아래까지 다시 실행된다는 뜻이다.

# ↑여기에는 우리가 나중에 배울 내용이 '함축' 되어 있다.

# 고맙게도(?)  Streamlit 에는 cache 메커니즘도 제공한다
#   => 어떤것은 다시 실행되지 않도록 할수도 있다.
#   (나중에 우리가 첫번째 Chatbot 을 구현할때 보게 될겁니다.)

value = st.slider(label='temperature', min_value=0.1, max_value=1.0)
st.text(value)

# 특정 값에 따라 보여지거나  보여지지 않거나 를 지정해주기

if model == 'GPT-3':
    st.write('cheap')
else:
    st.write('expensive')
    country = st.text_input('What is your country?')
    st.write(country)

# 버튼
# 눌렸을때 True 리턴.
button = st.button('버튼을 클릭해보세요')
if button:
    st.write(":blue[버튼] 이 불렸습니다 :sparkles:")

# 다운로드 버튼
# st.download_button() => bool 리턴
#  버튼을 클릭하면 다운로드

# 파일 다운로드 버튼. 
# 샘플 데이터 생성
df = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
})

st.download_button(
    label="CSV로 다운로드",
    data=df.to_csv(),
    file_name = 'sample.csv',
    mime='text/csv',
)

# st.download_button(
#     label='xlsx로 다운로드',
#     data=df.to_excel(),
#     file_name = 'sample.xlsx',
#     mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
# )


# 체크박스
# st.checkbox() => bool 리턴
agree = st.checkbox('동의 하십니까?')

if agree:
    st.write("동의 해주셔서 감사합니다 :100:")

# st.radio() => 선택한 option 객체,  혹은 None 리턴
# 라디오 선택 버튼

mbti = st.radio(
    label="당신의 MBTI는 무엇입니까?",
    options=('ISTJ', "ENFP", '선택지 없슴'),
)

st.write({
    'ISTJ': '당신은 :blue[현실주의자] 입니다',
    'ENFP': '당신은 :green[활동가] 입니다',
    '선택지 없슴': '당신에 대해 :red[알고 싶어요]:grey_exclamation:'
}[mbti])

# ---------------------------------------------------
# st.selectbox() => 선택한 option 객체,  혹은 None 리턴
# 선택 박스
mbti = st.selectbox(
    label='당신의 MBTI는 무엇입니까?',
    options=('ISTJ', 'ENFP', '선택지 없음'),
    index=2,
)

if mbti == 'ISTJ':
    st.write('당신은 :blue[현실주의자] 이시네요')
elif mbti == 'ENFP':
    st.write('당신은 :green[활동가] 이시네요')
else:
    st.write("당신에 대해 :red[알고 싶어요]:grey_exclamation:")

# 다중선택
# st.multiselect() => list

options = st.multiselect(
    label="당신이 좋아하는 과일은 뭔가요?",
    options=['망고', '오렌지', '사과', '바나나'],
    default=['망고', '오렌지'],
)

st.write(f'당신의 선택은: :red[{options}] 입니다')

# st.slider => tuple 을 지정하면 범위값 지정 가능. 이경우 tuple 리턴함
# 슬라이더
values = st.slider(
    label='범위의 값을 다음과 같이 지정할 수 있어요:sparkles:',
    min_value=0.0,
    max_value=100.0,
    value=(25.0, 75.0),
)
st.write('선택 범위:', values)


from datetime import datetime as dt 
import datetime

meeting_time = st.slider(
    label="약속을 언제로 잡을까요?",
    min_value=dt(2020, 1, 1, 0, 0),
    max_value=dt(2020, 1, 7, 23, 0),
    value=dt(2020, 1, 3, 12, 0),
    step=datetime.timedelta(hours=1),
    format="MM/DD/YY - HH:mm",
)
st.write("선택한 약속시간:", meeting_time)

# st.text_input => str 리턴
# 텍스트 입력.  (입력후  ENTER 하면 리턴값)
title = st.text_input(
    label='가고 싶은 여행지가 있나요?',
    placeholder='여행지를 입력해 주세요',
)
st.write(f'당신이 선택한 여행지: :violet[{title}]')

# st.number_input => int / float / None 리턴
# 숫자 입력
number = st.number_input(
    label='나이를 입력해 주세요.',
    min_value = 10,
    max_value=100,
    value=30,
    step=5,
)
st.write('당신이 입력하신 나이는: ', number)


# 로또 생성기
import random

st.markdown('---')
st.title(':sparkles:로또생성기:sparkles:')

def generate_lotto():
    lotto = [i + 1 for i in range(45)]
    random.shuffle(lotto)
    return lotto[:6]

button = st.button('로또를 생성해 주세요!')

if button:
    for i in range(1, 6):
        st.subheader(f'{i} 행운의 번호: :green[{generate_lotto()}]')


# 파일 업로더 위젯
st.markdown('---')
st.title('파일 업로드:sparkles:')

# ----------------------------------------------
# st.file_uploader() => None | UploadedFile | list of UploadedFile 리턴
# 파일 업로드 버튼 (업로드 기능)

file = st.file_uploader(
    "파일 선택(csv or excel)",
    type=['csv', 'xls', 'xlsx'],
)

# if file:
#     # 파일 읽기
#     df = pd.read_csv(file)
#     st.dataframe(df)

# ※ 간혹.. 403 에러가 뜨기도 한다..  다시 읽어들이면 될거다
# 오류를 방지하기 위해선 약간의 delay 를 주든가
#  혹은 spinner 같은 것을 두어 업로드 대기 시간을 주면 되긴 하다.
import time
time.sleep(1)

# Excel or CSV 확장자를 구분하여 출력하는 경우
if file:
    ext = file.name.split('.')[-1]  # 확장자

    if ext == 'csv':
        df = pd.read_csv(file)
        st.dataframe(df)
    elif 'xls' in ext:   # 'xls' 혹은 'xlsx'
        df = pd.read_excel(file, engine='openpyxl')
        st.dataframe(df)































