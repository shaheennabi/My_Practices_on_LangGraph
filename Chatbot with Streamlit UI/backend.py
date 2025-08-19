from langgraph.graph import  StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import  BaseMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory  import InMemorySaver
from langgraph.graph.message import add_messages
from dotenv import load_dotenv


load_dotenv()

llm = ChatOpenAI()

class ChatState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def chat_node(state: ChatState):
    messages = state['messages']
    response = llm.invoke(messages)
    return  {"messages": [response]}

## checkpointer
checkpointer = InMemorySaver()

## creating instance of StateGraph
graph = StateGraph(ChatState)

## adding the node
graph.add_node("chat_node", chat_node)

## adding edges
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)


## compiling
chatbot = graph.compile(checkpointer=checkpointer)