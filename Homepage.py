import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage

# initialize ChatOpenAI object
chat = None

if "OPENAI_API_KEY" not in st.session_state:
    st.session_state["OPENAI_API_KEY"] = ""
else:
    chat = ChatOpenAI(openai_api_key=st.session_state["OPENAI_API_KEY"], openai_api_base="https://api.deepseek.com/v1", model_name="deepseek-reasoner")

if "PINECONE_API_KEY" not in st.session_state:
    st.session_state["PINECONE_API_KEY"] = ""
if "PINECONE_ENVIRONMENT" not in st.session_state:
    st.session_state["PINECONE_ENVIRONMENT"] = ""


st.set_page_config(page_title="Homepage Welcome Streamlit-langchain", layout="wide")

st.title("Welcome to Streamlit-langchain")


with st.container():
    st.header("OpenAI Settings")
    st.markdown(f"""
                | OpenAI API Key |
                |----------------|
                | {st.session_state["OPENAI_API_KEY"]} |
                """)

with st.container():
    st.header("PineCone Settings")
    st.markdown(f"""
                | PineCone API Key | PineCone Environment |
                |------------------|----------------------|
                | {st.session_state["PINECONE_API_KEY"]} | {st.session_state["PINECONE_ENVIRONMENT"]} |
                """)
    
if "messages" not in st.session_state:
    st.session_state.messages = []



if chat:
    with st.container():
        st.header("Test OpenAI Chat Model")
        for message in st.session_state.messages:
            if message["role"] == "user":
                with st.chat_message("user"):
                    st.markdown(message["content"])
            elif message["role"] == "assistant":
                with st.chat_message("assistant"):
                    st.markdown(message["content"])

        user_input = st.chat_input("Type your message here...", key="chat_input")
        if user_input:
            with st.chat_message("user"):
                st.markdown(f"{user_input}")
            response = chat([HumanMessage(content=user_input)])
            with st.chat_message("assistant"):
                st.markdown(f"{response.content}")
            st.session_state.messages.append({"role": "assistant", "content": response.content})
            st.session_state.messages.append({"role": "user", "content": user_input})

else:
    with st.container():
        st.warning("Please set your OpenAI API Key in the OpenAI Settings page to test the chat model.")