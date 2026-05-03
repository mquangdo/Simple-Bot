from typing import Annotated, Sequence, TypedDict
from langchain_core.messages import BaseMessage, AIMessage, ToolCall, ToolMessage, SystemMessage # The foundational class for all message types in LangGraph
from langchain_core.tools import tool
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel, Field



class AgentState(TypedDict):
    """
    State definition for the ReAct agent.

    Attributes:
        messages: List of messages in the conversation (HumanMessage, AIMessage, ToolMessage)
    """
    messages: Annotated[Sequence[BaseMessage], add_messages]
