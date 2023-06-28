import streamlit as st
import openai
import os

# Set OpenAI API key
openai.api_key = os.environ["OPENAI_API_KEY"]

st.set_page_config(page_title="True or False", page_icon=":robot:")
st.sidebar.header("ChatGPT True or False")

st.sidebar.markdown("Ask ChatGPT any question and it will answer **True** or **False**")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("Your message"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            logit_bias={
                '2575': 100,
                '4139': 100
            },
            max_tokens=1,
            temperature=0,
            stream=True,
        ):
            full_response += response.choices[0].delta.get("content", "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append({"role": "assistant", "content": full_response})
