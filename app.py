import streamlit as st
import logging
import time
from src.agent import create_agent, query_agent

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

st.set_page_config(
    page_title="Financial Data Chatbot",
    page_icon="📊",
    layout="centered"
)

st.title("📊 Financial Data Chatbot")
st.caption("Ask questions about holdings and trades data • Powered by AI")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "agent" not in st.session_state:
    try:
        with st.spinner("Loading data and initializing agent..."):
            agent, memory = create_agent()
            st.session_state.agent = agent
            st.session_state.memory = memory
            st.success("✓ Agent initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize agent: {e}", exc_info=True)
        st.error(f"Failed to initialize agent: {str(e)}")
        st.stop()

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handle user input
prompt = st.chat_input("Ask a question about the data...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        try:
            # Show thinking indicator
            with st.spinner("🔍 Analyzing data..."):
                response = query_agent(st.session_state.agent, prompt)
            
            # Stream the response character by character for visual effect
            response_placeholder = st.empty()
            displayed = ""
            for char in response:
                displayed += char
                response_placeholder.markdown(displayed + "▌")
                time.sleep(0.008)  # Small delay for streaming effect
            
            # Final response without cursor
            response_placeholder.markdown(displayed)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            logger.error(f"Error during query: {e}", exc_info=True)
            error_msg = "Sorry, an error occurred while processing your question."
            st.error(error_msg)
            st.session_state.messages.append({"role": "assistant", "content": error_msg})

# Sidebar with info
with st.sidebar:
    st.markdown("### ℹ️ About")
    st.markdown("""
    This chatbot answers questions about:
    - **Holdings data**: Portfolio positions, market values, P&L
    - **Trades data**: Buy/sell transactions, custodians
    
    The bot only answers from the provided data files.
    """)
    
    st.markdown("---")
    st.markdown("### 📝 Conversation Memory")
    st.markdown(f"Messages in context: {len(st.session_state.messages)}")
    
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.messages = []
        if "memory" in st.session_state:
            st.session_state.memory.clear()
        st.rerun()
