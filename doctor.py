import streamlit as st 
from AppController import AskAQuestion
st.title("Chatbox: Hỏi đáp y tế")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        print(message)

# React to user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = AskAQuestion(prompt)
    if response is None:
        response = "Sorry, I can't help you with that."

    f"""### CYPHER QUERY: 
    ```cypher
    {response['query']}
    ```"""
    "### QUERY RESULT: "
    response["queryResult"]

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        st.markdown(response["answer"])
    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response["answer"]})