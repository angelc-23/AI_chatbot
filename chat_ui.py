"""Chat interface component for the Streamlit app."""
import streamlit as st
from rag import ask_rag


# ---------- INIT ----------
def init_chat_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []


# ---------- RENDER CHAT ----------
def render_chat_interface():
    for message in st.session_state.messages:
        avatar = "🤖" if message["role"] == "assistant" else "😎"

        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


# ---------- ADD MESSAGE ----------
def add_message(role, content):
    st.session_state.messages.append({
        "role": role,
        "content": content
    })


# ---------- INPUT BOX ----------
def chat_input_box():
     user_input = st.chat_input("💬 Ask your question...")

     if user_input:
        # ✅ add user message
        st.session_state.messages.append({
            "role": "user",
            "content": user_input
        })

        # ✅ get answer
        answer = ask_rag(user_input)

        # ✅ add bot response
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer
        })

        st.rerun()
