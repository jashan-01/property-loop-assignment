import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_experimental.agents import create_pandas_dataframe_agent
from src.data_loader import load_data
from src.prompts import SYSTEM_PROMPT

load_dotenv()


def create_agent():
    holdings_df, trades_df = load_data()
    
    llm = ChatOpenAI(
        model="gpt-4",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY")
    )
    
    agent = create_pandas_dataframe_agent(
        llm=llm,
        df=[holdings_df, trades_df],
        prefix=SYSTEM_PROMPT,
        verbose=False,
        allow_dangerous_code=True,
        agent_executor_kwargs={"handle_parsing_errors": True}
    )
    
    return agent


def query_agent(agent, question: str) -> str:
    try:
        response = agent.invoke({"input": question})
        return response.get("output", "Sorry can not find the answer")
    except Exception as e:
        return "Sorry can not find the answer"
