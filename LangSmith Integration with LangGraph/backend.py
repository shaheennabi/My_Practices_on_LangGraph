# backend.py
from typing import TypedDict, Annotated
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
import sqlite3





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



conn = sqlite3.connect(database="chatbot.db", check_same_thread=False)


# Create checkpointer
checkpointer = SqliteSaver(conn=conn)

# Build graph
graph = StateGraph(ChatState)

# Add nodes and edges
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

# Compile into runnable chatbot
chatbot = graph.compile(checkpointer=checkpointer)


##  retrieve threads from db
def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])
        
    return list(all_threads)