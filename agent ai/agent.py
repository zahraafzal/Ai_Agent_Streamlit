from langchain.agents import create_agent
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver
from serpapi import GoogleSearch
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

llm = ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0.7,
    max_retries=2,
    api_key=os.getenv("GROQ_API_KEY")
)


def serpapi_search(query: str):
    """searches for a query using the serpapi on google"""
    params = {
        "q": query,
        "hl": "en",
        "gl": "us",
        "api_key": os.getenv("SERP_API_KEY")
    }
    search = GoogleSearch(params)
    results = search.get_dict()
    
  
    if "organic_results" in results:
        return [
            {"title": r["title"], "link": r["link"], "snippet": r.get("snippet", "")}
            for r in results["organic_results"][:5]
        ]
    return {"error": "No results found"}

memory = InMemorySaver()

agent = create_agent(
    model = llm,
    tools = [serpapi_search],
    system_prompt = "You are a helpful assistant",
    checkpointer = memory
)
print("🤖 Agent starting...")
print("📝 Query: What is dollar current rate today in pakistan in 10 may 2026")

response = agent.invoke(
    {"messages": [{"role": "user", "content": "What is dollar current rate today in pakistan in 10 may 2026"}]},
    config={"configurable": {"thread_id": "user123"}}
)

print("\n✅ Response received:")
print(response['messages'][-1].content)