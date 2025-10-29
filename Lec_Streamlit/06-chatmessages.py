import streamlit as st
import time

# Chat elements 
#  공식] https://docs.streamlit.io/develop/api-reference/chat

st.set_page_config(
    page_title="Chat Message",
    page_icon="👀",
)

st.title("Chat Messages")

# chat_message()  : chat message container 생성
#             human 혹은 AI 모두에게서 받을수 있다.
#     매개변수는 'user', 'assistant', 'ai', 'human' 중 하나


if 'messages' not in st.session_state:
    st.session_state['messages'] = []

# st.write(st.session_state['messages']) # 확인 출력    


# 챗 입력 위젯
message = st.chat_input(placeholder="Send a message to AI")

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.write(message)

    if save:
        st.session_state['messages'].append({'message': message, 'role': role})

# 화면에 chat history 그리기
for msg in st.session_state['messages']:
    send_message(msg['message'], msg['role'], save=False)


if message:
    send_message(message, 'human')        
    time.sleep(2)
    send_message(f'You said: {message}', 'ai')

    with st.sidebar:
        st.write(st.session_state['messages'])

# refresh 되더라도 상태값을 기억하도록
# streamlit 에서는 session state 제공.
# session state 는 여러번 재실행해도 data 가 보존될수 있도록 해준다.

# session_state 는 여러번 재실행해도 data 가 보존될수 있도록 해준다.
#   보존되는 데이터는 key-value 형태로 session에 저장됨






# --------------------------------------------------
# status : Insert a status container to display output from long-running tasks.
#  시간이 오래걸리는 작업에 대해서 진행 status(상태) 표시 위젯

# import time

# with st.status("Embedding file...", expanded=True) as status:
#     time.sleep(3)
#     st.write("Getting the file")
#     time.sleep(3)
#     st.write("Embedding the file")
#     time.sleep(3)
#     st.write("Caching the file")
#     status.update(label="Error", state="error")









