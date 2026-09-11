import streamlit as st
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage, SystemMessage
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

st.title("AI Search Agent")
st.caption("Ask me anything and I'll search the web for you!")
st.divider()

# Check API keys
groq_key = os.getenv("GROQ_API_KEY")
serp_key = os.getenv("SERP_API_KEY")

if not groq_key:
    st.error("❌ GROQ_API_KEY not found")
    st.stop()

# Initialize LLM
@st.cache_resource
def get_llm():
    return ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.7,
        api_key=groq_key
    )

# Search function
def search_web(query):
    """Search using SerpAPI"""
    if not serp_key:
        return None
    
    try:
        params = {
            "q": query,
            "hl": "en",
            "gl": "us",
            "api_key": serp_key
        }
        search = GoogleSearch(params)
        results = search.get_dict()
        
        if "organic_results" in results:
            search_results = []
            for r in results["organic_results"][:3]:
                search_results.append(f"**{r['title']}**\n{r.get('snippet', '')}\n{r['link']}\n")
            return "\n".join(search_results)
    except:
        return None
    
    return None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
user_input = st.chat_input("Ask me anything...")

if user_input:
    # Add user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    with st.chat_message("user"):
        st.write(user_input)
    
    # Generate response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Thinking..."):
            try:
                llm = get_llm()
                
                # Try to search web first
                search_results = search_web(user_input)
                
                # Create prompt
                if search_results:
                    prompt = f"""You are a helpful AI assistant. Use the following web search results to answer the question.

Search Results:
{search_results}

Question: {user_input}

Provide a clear and concise answer based on the search results."""
                else:
                    prompt = f"You are a helpful AI assistant. Answer this question: {user_input}"
                
                # Get response from LLM
                response = llm.invoke([
                    SystemMessage(content="You are a helpful assistant."),
                    HumanMessage(content=prompt)
                ])
                
                st.write(response.content)
                st.session_state.messages.append({"role": "assistant", "content": response.content})
                
            except Exception as e:
                error_msg = f"❌ Error: {str(e)}"
                st.error(error_msg)
                st.session_state.messages.append({"role": "assistant", "content": error_msg})
