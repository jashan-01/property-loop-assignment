import streamlit as st
from src.agent import create_agent, query_agent

st.set_page_config(
    page_title="Financial Data Chatbot",
    page_icon="📊",
    layout="centered"
)

st.title("Financial Data Chatbot")
st.caption("Ask questions about holdings and trades data")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    with st.spinner("Loading data and initializing agent..."):
        st.session_state.agent = create_agent()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask a question about the data..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            response = query_agent(st.session_state.agent, prompt)
        st.markdown(response)
    
    st.session_state.messages.append({"role": "assistant", "content": response})
