# backend.py
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv

# load .env for OpenAI key
load_dotenv()

# Initialize model
llm = ChatOpenAI(model="gpt-3.5-turbo")  

# Define state schema
class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]

# Node function
def chat_node(state: ChatState):
    messages = state["messages"]
    response = llm.invoke(messages)   # LLM sees full history
    return {"messages": [response]}   # append new AI message to state

# Create checkpointer
checkpointer = InMemorySaver()

# Build graph
graph = StateGraph(ChatState)

# Add nodes and edges
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile into runnable chatbot
chatbot = graph.compile(checkpointer=checkpointer)


