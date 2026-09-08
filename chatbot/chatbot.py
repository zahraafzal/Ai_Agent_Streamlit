import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

st.title("🤖 ChatBot")
st.caption("Ask anything below")
st.divider()

# Get API key from Streamlit secrets (for deployment) or .env file (for local)
try:
    api_key = st.secrets["GROQ_API_KEY"]
except:
    api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    st.error("❌ GROQ_API_KEY not found")
    st.info("💡 Please add GROQ_API_KEY to secrets.toml or .env file")
    st.stop()

# Chat input
user_input = st.chat_input("Type your message...")

# If user enters a message
if user_input:
    try:
        llm = ChatGroq(
            model="openai/gpt-oss-20b",
            temperature=0,
            api_key=api_key,
        )

        # Show user message
        st.chat_message("user").write(user_input)

        # Generate response
        with st.spinner("Thinking..."):
            response = llm.invoke([
                SystemMessage(content="You are a helpful assistant."),
                HumanMessage(content=user_input)
            ])

        # Show assistant response
        st.chat_message("assistant").write(response.content)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
        st.info("💡 Make sure your Groq API key is valid.")
