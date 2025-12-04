import os
from langchain_openai.chat_models.base import ChatOpenAI
from langchain.agents.agent_types import AgentType

from dotenv import load_dotenv
load_dotenv()

# sql agent 생성 함수
from langchain_community.agent_toolkits.sql.base import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase

file_dir = os.path.dirname(os.path.realpath(__file__))
db_path = os.path.join(file_dir, "movies.sqlite")

# DB파일로부터 SQLDatabase 생성
db = SQLDatabase.from_uri(f'sqlite:///{db_path}')

# toolkit 생성 (db 와 LLM 으로부터 생성)
llm = ChatOpenAI(temperature=0.1)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)

# agent 생성 (LLM 과 toolkit 으로부터 생성)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,  # toolkit 지정!
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# agent 호출
# agent.invoke("Give me 5 directors that have the highest grossing films.")

# "평점은 가장 높지만 예산이 낮았던 영화를 알려줘. 감독의 이름도!"
# agent.invoke("Give me the movies that have the lowest budgets but the highest votes, and give me the name of their directors also include their gross revenue")

print(toolkit.get_tools())























