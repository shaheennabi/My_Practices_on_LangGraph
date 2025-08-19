import streamlit as st
from backend import chatbot
from langchain_core.messages import HumanMessage

## config
config = {'configurable': {'thread_id': "thread-1"}}

## st.session -> dict -> never erase
if "message_history" not in st.session_state:
    st.session_state['message_history'] = []

## loading the conversation history
for message in st.session_state['message_history']:
    with st.chat_message(message['role']):
        st.text(message['content'])

user_input = st.chat_input('Type here')

if user_input:
    ## first adding message to message history
    st.session_state['message_history'].append({'role': "user", "content": user_input})
    with st.chat_message('user'):
        st.text(user_input)

    # invoke chatbot
    response = chatbot.invoke({'messages': [HumanMessage(content=user_input)]}, config=config)

    # FIXED: response is a dict of state, not AIMessage
    ai_message = response["messages"][-1].content

    ## adding message to message history
    st.session_state['message_history'].append({'role': "assistant", "content": ai_message})
    with st.chat_message('assistant'):
        st.text(ai_message)
