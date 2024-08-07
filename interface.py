import streamlit as st
from chatbot import main_input

import requests


def send_message(message, user_id):
    url = "http://localhost:8000/process"
    data = {"message": message, "user_id": user_id}
    response = requests.post(url, json=data)
    return response.json()

st.sidebar.header("Current User.")
user_id = st.sidebar.text_input("Enter User ID" , value="52700585-5642-4366-aded-a9896af705b9")

# st.header("App Assistant")
# question = st.chat_input("Enter your query")

# if not user_id:
#     st.warning("Please provide user ID.")
# else:
#     if question:
#         embedding_pipeline(user_id)
#         result = main_input(question,user_id)
#         st.write(result)

if 'messages' not in st.session_state:
    st.session_state.messages = []

# Display any previous chat messages in the chat window
for message in st.session_state.messages:
    with st.chat_message(message['role']):
        st.markdown(message['content'])

# Display chat input box and 
# check to see if the user (you) entered in a message
if prompt := st.chat_input("Enter Your Query."):
    # If user entered a message, add it to chat list.
    
    st.session_state.messages.append({ 'role': 'user', 'content': prompt })
    

    # Display user's submitted message
    with st.chat_message('user'):
        st.markdown(prompt)
    # embedding_pipeline(user_id)
    
    result = send_message(prompt,user_id)
    st.session_state.messages.append({ 'role': 'assistant', 'content': result })
    with st.chat_message('assistant'):
        st.markdown(result)
    # message_placeholder.markdown(result)

    # Add assistant's response to chat msg's list
    





