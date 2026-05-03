from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, ToolCall, ToolMessage, SystemMessage # The foundational class for all message types in LangGraph
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field



class ArgWebSearchSchema(BaseModel): #can work like LangChain (tool decorator)
    """
    Input schema for the web search tool.
    
    Attributes:
        query: The search query to look up on the web.
    """
    query: str = Field(
        description="The search query to look up on the web.", 
        default="What is the capital of France?"
    )
    
