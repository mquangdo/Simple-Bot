import traceback
from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, ToolCall, ToolMessage, SystemMessage # The foundational class for all message types in LangGraph
from langchain_core.tools import tool, StructuredTool
from langchain_tavily import TavilySearch
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field
from schema import ArgWebSearchSchema
from dotenv import load_dotenv

load_dotenv()



class AgentTool:
    
    @staticmethod 
    def websearch_tool(query: str) -> str: 
        """
        Perform a web search for the given query and return the results.
        
        Args:
            query (str): The search query.
        Returns:
            str: The search results as a string.
        """

        tavily_search = TavilySearch(
            num_results=3,  # Number of search results to return
        )

        result = tavily_search.invoke(query)
        # print(result) 
        # formatted_results = []

        # for i, item in enumerate(result):
        #     content  = f"Result {i+1}:\n"
        #     content += f"Title: {item['title']}\n"
        #     content += f"Description: {item['content']}\n\n"
        #     formatted_results.append(content)

        return result['results'][0]['content'] if result['results'] else "No results found."
            

def get_tools():
    
    agent_tools = [
        StructuredTool.from_function(
            func=AgentTool.websearch_tool, 
            name="websearch_tool", 
            description="A tool for performing web searches. Use this tool to find information on the web based on a search query.",
            args_schema=ArgWebSearchSchema
        )
            
    ]
    
    return agent_tools


if __name__ == "__main__":
    web_search_query = "Who is Quang Hung Do?"
    web_search_tool = AgentTool.websearch_tool(web_search_query)

    print(web_search_tool)
