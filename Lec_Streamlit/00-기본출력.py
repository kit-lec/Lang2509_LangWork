import streamlit as st
import numpy as np
import pandas as pd

import os
import time

from dotenv import load_dotenv
load_dotenv()

print(f'✅ {os.path.basename( __file__ )} 실행됨 {time.strftime('%Y-%m-%d %H:%M:%S')}')  # 실행파일명, 현재시간출력
print(f'\tOPENAI_API_KEY={os.getenv("OPENAI_API_KEY")[:20]}...') # 필요한 환경변수

# 서버 실행
# > streamlit run ******.py
#    ※ 초반에 email 물어보면 걍 엔터 치세요.

# 서버 종료
# 터미널창에서 user break (CTRL + C) 연타
# user break 되지 않으면 terminal 종료(kill) 하세요

# 기본적인 widget(ui)

# 타이틀 적용 예시
st.title('기본 출력')

# 특수 이모티콘 삽입 예시
# emoji: https://streamlit-emoji-shortcodes-streamlit-app-gwckff.streamlit.app/
st.title('스마일 :sunglasses:')

# Header 적용
st.header('헤더를 입력할 수 있어요! :sparkles:')

# SubHeader 적용
st.subheader('이것은 subheader 입니다')

# 캡션 적용
st.caption('캡션을 추가해봅니다')

# 코드 표시
sample_code = '''
def function():
    print('hello, world')
'''

st.code(sample_code, language='python')

# 일반 텍스트
st.text("일반적인 텍스트")

# 마크다운 문법
st.markdown("streamlit 은 **마크다운 문법을 지원** 합니다")
st.markdown("텍스트의 색상을 :green[초록색]으로, 그리고 **:blue[파란색]** 볼드체로 설정")
st.markdown(r":green[$\sqrt{x^2+y^2}$] 와 같이 latex 문법의 수식 표현 가능")

# latex() 함수
st.latex(r'\sqrt{x^2+y^2}')

# <hr> 가로선
st.markdown('---')

# DataFrame
dataframe = pd.DataFrame({
    'first column': [1, 2, 3, 4],
    'second column': [10, 20, 30, 40],
})


# DataFrame
# use_container_width 기능은 데이터프레임을 컨테이너 크기에 확장할 때 사용합니다. (True/False)
st.dataframe(dataframe, use_container_width=True)
st.dataframe(dataframe, use_container_width=False)

# 테이블(static)
# DataFrame과는 다르게 interactive 한 UI 를 제공하지 않습니다.
st.table(dataframe)

# 메트릭
st.metric(label="온도", value="10C", delta="1.2C")
st.metric(label="삼성전자", value="91,000원", delta="-1,200원")

st.markdown('---')

# 🟦 Magic
st.title('write()')

# 매개변수로 넘겨진건 '무엇이든' 화면에 그리려 한다.
st.write("hello")  # 텍스트
st.write([1, 2, 3, 4])
st.write({"x": 100, "y": 200})

# 클래스도 출력
import re

st.write(re.Pattern)

# 굳이 write() 사용하지 않아도 코드상의 값들을 화면에 그림
# 그래도 write() 를 명시적으로 사용하는 것을 추천함.
[1, 2, 3, 4]
{'name': 'John', 'age': 34}

# 🟦 Chart, Graph
st.title('Chart 그리기')

import matplotlib.pyplot as plt
import seaborn as sns

# 한글폰트 설정
from matplotlib import font_manager, rc
import platform
try : 
    if platform.system() == 'Windows':
    # 윈도우인 경우
        font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
        rc('font', family=font_name)
    else:    
    # Mac 인 경우
        rc('font', family='AppleGothic')
except : 
    pass
plt.rcParams['axes.unicode_minus'] = False 

df = pd.DataFrame({
    '이름': ['영식', '철수', '영희'],
    '나이': [22, 31, 25],
    '몸무게': [75.5, 80.2, 55.1],
})

st.dataframe(df, use_container_width=True)

# -------------------------------------------------
# st.pyplot(figure)
#  matplotlib.pyplot.figure 를 그린다.
#  시각화 라이브러리로 matplotlib 이나 seaborn 을 사용하게 될텐데.
#  이 경우 pyplot() 을 사용하여 그리면 된다.

fig, ax = plt.subplots()
ax.bar(df['이름'], df['나이'])
st.pyplot(fig)

barplot = sns.barplot(data=df, x='이름', y='나이', hue='이름', ax=ax, palette='Set2')
fig = barplot.get_figure()
st.pyplot(fig)

#############
# matplotlib 의 gallery 에 많은 예제들 
# https://matplotlib.org/stable/gallery/index.html
# 

# 그 중에 하나 예시를 가져와보자.
# Stacked bar chart 
# https://matplotlib.org/stable/gallery/lines_bars_and_markers/bar_stacked.html#sphx-glr-gallery-lines-bars-and-markers-bar-stacked-py


species = (
    "Adelie\n $\\mu=$3700.66g",
    "Chinstrap\n $\\mu=$3733.09g",
    "Gentoo\n $\\mu=5076.02g$",
)
weight_counts = {
    "Below": np.array([70, 31, 58]),
    "Above": np.array([82, 37, 66]),
}
width = 0.5

fig, ax = plt.subplots()
bottom = np.zeros(3)

for boolean, weight_count in weight_counts.items():
    p = ax.bar(species, weight_count, width, label=boolean, bottom=bottom)
    bottom += weight_count

ax.set_title("Number of penguins with above average body mass")
ax.legend(loc="upper right")

st.pyplot(fig)

##### Barcode 생성예제
# https://matplotlib.org/stable/gallery/images_contours_and_fields/barcode_demo.html


code = np.array([
    1, 0, 1, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 1, 1,
    0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0,
    1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 1, 1, 0, 0, 1,
    1, 0, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1])

pixel_per_bar = 4
dpi = 100

fig = plt.figure(figsize=(len(code) * pixel_per_bar / dpi, 2), dpi=dpi)
ax = fig.add_axes([0, 0, 1, 1])  # span the whole figure
ax.set_axis_off()
ax.imshow(code.reshape(1, -1), cmap='binary', aspect='auto',
          interpolation='nearest')

st.pyplot(fig)





























