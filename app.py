import streamlit as st
from core.chain5 import run_chain
from core.memory2 import create_chat

# -----------------------
# PAGE CONFIG
# -----------------------
st.set_page_config(
    page_title="BookMind AI",
    page_icon="📚",
    layout="wide"
)

# -----------------------
# SESSION INIT
# -----------------------
if "chat_id" not in st.session_state:
    st.session_state.chat_id = create_chat()

if "messages" not in st.session_state:
    st.session_state.messages = []

# -----------------------
# SIDEBAR
# -----------------------
with st.sidebar:
    st.title("📚 BookMind AI")

    st.markdown("""
    ### 🧠 About
    This AI answers ONLY from your uploaded books.

    ### 📖 Available Knowledge
    - AI Book  
    - Leadership Book  
    - Entrepreneurship Book  

    ### ⚙️ Features
    - RAG-based answers  
    - Memory support  
    - Context-aware responses  
    """)

    if st.button("🔄 New Chat"):
        st.session_state.chat_id = create_chat()
        st.session_state.messages = []
        st.rerun()

# -----------------------
# MAIN TITLE
# -----------------------
st.title("🤖 BookMind AI Assistant")
st.caption("Ask questions from your books 📖")

# -----------------------
# DISPLAY CHAT
# -----------------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# -----------------------
# USER INPUT
# -----------------------
user_input = st.chat_input("Ask something from your books...")

if user_input:

    # Show user message
    with st.chat_message("user"):
        st.markdown(user_input)

    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    # -----------------------
    # LOADING SPINNER
    # -----------------------
    with st.chat_message("assistant"):
        with st.spinner("Thinking... 🤔"):

            try:
                response = run_chain(st.session_state.chat_id, user_input)
            except Exception as e:
                response = f"❌ Error: {str(e)}"

        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })