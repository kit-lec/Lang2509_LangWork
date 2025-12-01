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


class CalculatorTool(BaseTool):
    name: Type[str] = "CalculatorTool"   # tool 이름에 공백 있으면 안됨!
    description: Type[str] = """
    Use this to perform sums of two numbers.
    The first and second arguments should be numbers.
    Only receives two arguments.
    """

    # TODO:  



llm = ChatOpenAI(temperature=0.1)

def plus(inputs):
    a, b = inputs.split(",")
    return float(a) + float(b)

agent = initialize_agent(
    llm=llm,
    verbose=True,
    agent=AgentType.OPENAI_FUNCTIONS,
    tools=[
        Tool.from_function(
            func=plus,
            name="Sum Calculator",
            description="Use this to perform sums of two numbers. Use this tool by sending a pair of numbers separated by a comma.\nExample:1,2",
        ),
    ],
)

prompt = "Cost of $355.39 + $924.87 + $721.2 + $1940.29 + $573.63 + $65.72 + $35.01 + $552.01 + $76.16 + $29.12"

agent.invoke(prompt)