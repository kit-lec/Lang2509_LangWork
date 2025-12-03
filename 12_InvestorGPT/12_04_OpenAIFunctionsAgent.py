import warnings
warnings.filterwarnings('ignore')

from dotenv import load_dotenv
load_dotenv()

from langchain_openai.chat_models.base import ChatOpenAI
from langchain.agents.initialize import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_core.tools.simple import Tool
from langchain_core.tools.base import BaseTool  # 커스텀 Tool 을 만들기 위해서 BaseTool 을 구현해야 한다

from pydantic import BaseModel, Field
from typing import Any, Type  # typing 은 Python 의 기본 내장모듈



# pydantic 의 BaseModel 구현. => 사용자 정의 데이터 모델 정의
#   - 입력데이터의 타입검증, 자동변환, 직렬화/역직렬화 등의 처리기능 제공됨.
class CalculatorToolArgsSchema(BaseModel):
    a: float = Field(description="The first number")
    b: float = Field(description="The second number")


class CalculatorTool(BaseTool):
    name: Type[str] = "CalculatorTool"   # tool 이름에 공백 있으면 안됨!
    description: Type[str] = """
    Use this to perform sums of two numbers.
    The first and second arguments should be numbers.
    Only receives two arguments.
    """

    # 매개변수 argument 의 구조(스키마) 정의 
    # argument 의 스키마를 정의하기 위해 별도의 pydantic Model 을 준비해봅니다 
    # argument 들은 이 스키마를 따르도록 지정
    #   => a 는 실수형, b 도 실수형
    args_schema: Type[CalculatorToolArgsSchema] = CalculatorToolArgsSchema

    # 이 툴이 사용되었을때 실행할 코드
    def _run(self, a, b):
        return a + b


llm = ChatOpenAI(temperature=0.1)

agent = initialize_agent(
    llm=llm,
    verbose=True,
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=[
        CalculatorTool()  # 커스텀 tool 지정
    ],
)

prompt = "Cost of $355.39 + $924.87 + $721.2 + $1940.29 + $573.63 + $65.72 + $35.01 + $552.01 + $76.16 + $29.12"

agent.invoke(prompt)