import streamlit as st
import FinanceDataReader as fdr
import datetime

st.title('주가정보')

print('✅ 실행됨')

# Finance Data Reader
# https://github.com/financedata-org/FinanceDataReader

start_date = st.date_input(
    '조회 시작일을 선택해 주세요',
    value = datetime.datetime(2025, 10, 10)
)

end_date = st.date_input(
    '조회 종료일을 선택해 주세요',
    value = datetime.datetime(2025, 10, 28)
)

code = st.text_input(
    '종목코드',
    value='005930',  
    placeholder='종목코드를 입력해주세요',
)

if code and start_date and end_date:
    df = fdr.DataReader(code, start_date, end_date)
    st.dataframe(df)
    st.line_chart(df['Close'])


































