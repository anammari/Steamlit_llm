import streamlit as st
import ollama
import boto3
import json

# Set up the page
st.set_page_config(page_title="LLM Chat App", initial_sidebar_state="expanded")
st.title("LLM Chat App")

# Sidebar for model selection
with st.sidebar:
    st.markdown("# Chat Options")
    model = st.selectbox('What model would you like to use?', ['phi4', 'aws-nova-micro'])

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User prompt input
user_prompt = st.chat_input("What would you like to ask?")

# File uploader
uploaded_file = st.file_uploader("Upload a file")

# If user submits a prompt
if user_prompt:
    # Display user prompt in chat message widget
    with st.chat_message("user"):
        st.markdown(user_prompt)

    # Add user's prompt to chat history
    st.session_state.messages.append({"role": "user", "content": user_prompt})

    # If a file is uploaded
    if uploaded_file is not None:
        # Read the file
        file_content = uploaded_file.read().decode("utf-8")

        # Combine chat history, user prompt and file content
        full_prompt = "\n\n".join([message["content"] for message in st.session_state.messages[:-1]]) + f"\n\nContext:\n{file_content}\n\nUser: {user_prompt}"
    else:
        full_prompt = "\n\n".join([message["content"] for message in st.session_state.messages[:-1]]) + f"\n\nUser: {user_prompt}"

    # Generate response from LLM
    with st.spinner('Generating response...'):
        if model == 'phi4':
            response = ollama.chat(model=model, messages=[{"role": "user", "content": full_prompt}])
            response_content = response['message']['content']
        elif model == 'aws-nova-micro':
            client = boto3.client(service_name="bedrock-runtime")
            messages = [
                {"role": "user", "content": [{"text": full_prompt}]},
            ]
            model_response = client.converse(
                modelId="us.amazon.nova-micro-v1:0",
                messages=messages
            )
            response_content = model_response["output"]["message"]["content"][0]["text"]

    # Display response in chat message widget
    with st.chat_message("assistant"):
        st.markdown(response_content)

    # Add response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})