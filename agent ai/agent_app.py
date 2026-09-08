import streamlit as st
from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.title("🔍 AI Search Agent")
st.caption("Ask me anything and I'll search the web for you!")
st.divider()

# Check API keys
groq_key = os.getenv("GROQ_API_KEY")
serp_key = os.getenv("SERP_API_KEY")

if not groq_key or not serp_key:
    st.error("❌ API Keys not found")
    st.info("💡 Please add GROQ_API_KEY and SERP_API_KEY to your .env file")
    st.stop()

# Initialize the LLM
@st.cache_resource
def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-120b",
        temperature=0.7,
        max_retries=2,
        api_key=groq_key
    )

# Define the search function
def serpapi_search(query: str):
    """searches for a query using the serpapi on google"""
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": serp_key
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
    if "organic_results" in results:
        return [
            {"title": r["title"], "link": r["link"], "snippet": r.get("snippet", "")}
            for r in results["organic_results"][:5]
        ]
    return {"error": "No results found"}

# Initialize agent
@st.cache_resource
def get_agent():
    llm = get_llm()
    memory = InMemorySaver()
    
    agent = create_agent(
        model=llm,
        tools=[serpapi_search],
        system_prompt="You are a helpful assistant that can search the web to answer questions accurately.",
        checkpointer=memory
    )
    return agent

# Initialize session state for chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Display user message
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching and thinking..."):
            try:
                agent = get_agent()
                response = agent.invoke(
                    {"messages": [{"role": "user", "content": user_input}]},
                    config={"configurable": {"thread_id": "streamlit_session"}}
                )
                
                assistant_response = response['messages'][-1].content
                st.write(assistant_response)
                
                # Add assistant response to chat history
                st.session_state.messages.append({"role": "assistant", "content": assistant_response})
                
            except Exception as e:
                error_msg = f"⚠️ Search unavailable. Answering without web search."
                st.warning(error_msg)
                
                # Fallback: Use LLM without search
                try:
                    llm = get_llm()
                    from langchain_core.messages import HumanMessage, SystemMessage
                    
                    fallback_response = llm.invoke([
                        SystemMessage(content="You are a helpful assistant. Answer based on your knowledge."),
                        HumanMessage(content=user_input)
                    ])
                    
                    st.write(fallback_response.content)
                    st.session_state.messages.append({"role": "assistant", "content": fallback_response.content})
                    
                except Exception as e2:
                    error_msg = f"❌ Error: {str(e2)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
