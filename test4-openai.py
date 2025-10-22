from dotenv import load_dotenv
load_dotenv()

from langchain_openai.chat_models.base import ChatOpenAI
chat = ChatOpenAI()  # <- OPENAI_API_KEY 환경변수가 설정되어 있어야 함.

result = chat.invoke("한국의 11월 날씨는 어떤가요?")
print(result)