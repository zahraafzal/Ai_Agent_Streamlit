# 🤖 AI Agent Streamlit

An intelligent AI agent powered by Groq LLM and SerpAPI that can search the web and answer questions through a beautiful Streamlit interface.

## Features

- 🔍 Web search capabilities using SerpAPI
- 💬 Interactive chat interface
- 🧠 Powered by Groq's GPT-OSS-120B model
- 📝 Chat history management
- ⚡ Fast and responsive

## Installation

1. Clone the repository:
```bash
git clone https://github.com/zahraafzal/Ai_Agent_Streamlit.git
cd Ai_Agent_Streamlit
```

2. Install dependencies:
```bash
pip install streamlit langchain-groq langgraph google-search-results python-dotenv
```

3. Create a `.env` file in the root directory:
```
GROQ_API_KEY=your_groq_api_key_here
SERP_API_KEY=your_serpapi_key_here
```

## Usage

### Run the Streamlit App:
```bash
streamlit run "agent ai/agent_app.py"
```

### Run the Command-line Agent:
```bash
python3 "agent ai/agent.py"
```

## API Keys

- **GROQ API Key**: Get it from [Groq Console](https://console.groq.com)
- **SerpAPI Key**: Get it from [SerpAPI](https://serpapi.com)

## Technologies Used

- **Streamlit** - Web interface
- **LangChain** - AI framework
- **Groq** - LLM provider
- **SerpAPI** - Web search
- **Python** - Programming language

## Author

Created by Zahra Afzal
