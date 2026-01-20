import os
import logging
from typing import Generator
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import create_react_agent, AgentExecutor
from langchain.tools import tool
from langchain import hub
from langchain.callbacks.base import BaseCallbackHandler
from src.data_loader import load_data
from src.prompts import SYSTEM_PROMPT, SUFFIX

# Setup logging
logger = logging.getLogger(__name__)
load_dotenv()


class StreamingCallbackHandler(BaseCallbackHandler):
    """Callback handler for streaming LLM responses."""
    
    def __init__(self):
        self.tokens = []
        self.is_final_answer = False
    
    def on_llm_new_token(self, token: str, **kwargs) -> None:
        """Collect tokens as they stream."""
        self.tokens.append(token)
    
    def on_agent_action(self, action, **kwargs) -> None:
        """Reset when agent takes an action (not final answer yet)."""
        self.is_final_answer = False
    
    def on_agent_finish(self, finish, **kwargs) -> None:
        """Mark when agent finishes with final answer."""
        self.is_final_answer = True
    
    def get_tokens(self):
        """Get collected tokens and clear."""
        tokens = self.tokens.copy()
        self.tokens = []
        return tokens


def create_agent(memory=None):
    """
    Create a LangChain ReAct agent for financial data analysis.
    """
    holdings_df, trades_df = load_data()
    
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
        api_key=os.getenv("OPENAI_API_KEY"),
        timeout=30,
        streaming=True
    )
    
    # Create DataFrame analysis tools
    @tool
    def query_holdings_data(pandas_code: str) -> str:
        """
        Execute pandas code to analyze holdings_df and return results.
        Available: holdings_df, pd (pandas)
        """
        try:
            import pandas as pd
            namespace = {
                "holdings_df": holdings_df,
                "pd": pd,
                "result": None
            }
            
            clean_code = pandas_code.strip()
            if clean_code.startswith("```"):
                clean_code = "\n".join(clean_code.split("\n")[1:-1])
            
            if "result =" not in clean_code and "print(" not in clean_code:
                clean_code = f"result = {clean_code}"
            
            exec(clean_code, {"__builtins__": {}}, namespace)
            result = namespace.get("result")
            if result is not None:
                return str(result)
            return "Error: No result returned"
        except Exception as e:
            return f"Error: {str(e)}"
    
    @tool
    def query_trades_data(pandas_code: str) -> str:
        """
        Execute pandas code to analyze trades_df and return results.
        Available: trades_df, pd (pandas)
        """
        try:
            import pandas as pd
            namespace = {
                "trades_df": trades_df,
                "pd": pd,
                "result": None
            }
            
            clean_code = pandas_code.strip()
            if clean_code.startswith("```"):
                clean_code = "\n".join(clean_code.split("\n")[1:-1])
            
            if "result =" not in clean_code and "print(" not in clean_code:
                clean_code = f"result = {clean_code}"
            
            exec(clean_code, {"__builtins__": {}}, namespace)
            result = namespace.get("result")
            if result is not None:
                return str(result)
            return "Error: No result returned"
        except Exception as e:
            return f"Error: {str(e)}"
    
    tools = [query_holdings_data, query_trades_data]
    
    # Use the official ReAct prompt template from LangChain hub
    prompt = hub.pull("hwchase17/react")
    
    # Update prompt with our system instruction
    prompt.template = SYSTEM_PROMPT + "\n\n" + prompt.template + "\n\n" + SUFFIX
    
    # Create the agent
    agent = create_react_agent(llm, tools, prompt)
    
    # Create executor with optimized settings
    agent_executor = AgentExecutor(
        agent=agent,
        tools=tools,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5,
        max_execution_time=60,
        early_stopping_method="force"
    )
    
    return agent_executor, None


def query_agent(agent, question: str) -> str:
    """
    Query the agent with better error handling and logging.
    """
    try:
        logger.info(f"Processing question: {question}")
        response = agent.invoke({"input": question})
        output = response.get("output", "")
        
        if not output:
            logger.warning("Agent returned empty output")
            return "Sorry can not find the answer"
        
        logger.info(f"Agent response received (length: {len(output)})")
        return output
    except TimeoutError:
        logger.error("Agent query timed out")
        return "Sorry can not find the answer"
    except Exception as e:
        logger.error(f"Agent error: {type(e).__name__}: {e}", exc_info=True)
        return "Sorry can not find the answer"


def query_agent_streaming(agent, question: str) -> Generator[str, None, None]:
    """
    Query the agent with streaming response.
    Yields tokens as they are generated.
    """
    try:
        logger.info(f"Processing question (streaming): {question}")
        
        full_response = ""
        
        # Use stream method for real-time token output
        for chunk in agent.stream({"input": question}):
            # The final output comes in the 'output' key
            if "output" in chunk:
                output = chunk["output"]
                if output:
                    for char in output:
                        yield char
                        full_response += char
        
        if not full_response:
            logger.warning("Agent returned empty output")
            yield "Sorry can not find the answer"
        else:
            logger.info(f"Agent streaming complete (length: {len(full_response)})")
            
    except TimeoutError:
        logger.error("Agent query timed out")
        yield "Sorry can not find the answer"
    except Exception as e:
        logger.error(f"Agent error: {type(e).__name__}: {e}", exc_info=True)
        yield "Sorry can not find the answer"
