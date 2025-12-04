from langchain_openai.chat_models.base import ChatOpenAI
from langchain.agents.initialize import initialize_agent
from langchain.agents.agent_types import AgentType
from langchain_core.tools.simple import Tool
from langchain_core.tools.base import BaseTool

from pydantic import BaseModel, Field
from typing import Any, Type

from langchain_community.utilities.duckduckgo_search import DuckDuckGoSearchAPIWrapper

import os
import requests

from dotenv import load_dotenv
load_dotenv()
alpha_vantage_api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
print(f'\tALPHA_VANTAGE_API_KEY={alpha_vantage_api_key[:5]}...')



llm = ChatOpenAI(temperature=0.1)

# 회사 심볼 tool
class StockMarketSymbolSearchToolArgsSchema(BaseModel):
    query: str = Field(
        description="The query you will search for.Example query: Stock Market Symbol for Apple Company"
    )

class StockMarketSymbolSearchTool(BaseTool):
    name: Type[str] = "StockMarketSymbolSearchTool"
    description: Type[str] = """
        Use this tool to find the stock market symbol for a company.
        It takes a query as an argument.
        Example query: Stock Market Symbol for Apple Company
        """
    
    args_schema: Type[StockMarketSymbolSearchToolArgsSchema] = StockMarketSymbolSearchToolArgsSchema

    def _run(self, query):
        ddg = DuckDuckGoSearchAPIWrapper()
        return ddg.run(query) # 검색결과(들)을 하나의 str 으로 묶어서 리턴.

# 회사 개요 tool
class CompanyOverviewArgsSchema(BaseModel):
    symbol: str = Field(
        description="Stock symbol of the company.Example: AAPL,TSLA",
    )

class CompanyOverviewTool(BaseTool):
    name: Type[str] = "CompanyOverview"
    description: Type[str] = """
    Use this to get an overview of the financials of the company.
    You should enter a stock symbol.
    """

    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def _run(self, symbol):
        response = requests.get(
            f"https://www.alphavantage.co/query?function=OVERVIEW&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        return response.json()   


# 손익계산서 (income statement) 툴
class CompanyIncomeStatementTool(BaseTool):
    name: Type[str]  = "CompanyIncomeStatement"
    description: Type[str]  = """
    Use this to get the income statement of a company.
    You should enter a stock symbol.
    """
    # ↑ 입력이 stock symbol 이기 때문에
    # ↓ CompanyOverviewArgsSchema을 그대로 사용해도 된다.
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def _run(self, symbol):
        response = requests.get(
            f"https://www.alphavantage.co/query?function=INCOME_STATEMENT&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        return response.json()["annualReports"]  

# 주간정보툴
class CompanyStockPerformanceTool(BaseTool):
    name: Type[str]  = "CompanyStockPerformance"
    description: Type[str]  = """
    Use this to get the weekly performance of a company stock.
    You should enter a stock symbol.
    """
    # ↑ 입력이 stock symbol 이기 때문에
    # ↓ CompanyOverviewArgsSchema을 그대로 사용해도 된다.
    args_schema: Type[CompanyOverviewArgsSchema] = CompanyOverviewArgsSchema

    def _run(self, symbol):
        response = requests.get(
            f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={alpha_vantage_api_key}"
        )
        return response.json()


agent = initialize_agent(
    llm=llm,
    verbose=True,
    agent=AgentType.OPENAI_FUNCTIONS,
    handle_parsing_errors=True,
    tools=[
        StockMarketSymbolSearchTool(),
        CompanyOverviewTool(),
        CompanyIncomeStatementTool(),
        CompanyStockPerformanceTool(),
    ],
)

prompt = "Give me information on Cloudflare's stock, considering its financials, income statements and stock performance and help me analyze if it's a potential good investment."

agent.invoke(prompt)
