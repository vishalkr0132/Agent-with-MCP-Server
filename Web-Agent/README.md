# 🕵️ Python MCP Agent with Groq + Serper Search

This project implements a modular chat plugin (MCP) search agent using the `agno` AI framework, the powerful **Groq LLaMA 3-70B Versatile** model, and **Serper.dev** (Google Search API). It performs web searches, processes results, and displays answers using markdown, with full source attribution and MCP-compliant formatting.

---

## 🚀 Features

- 🔍 Web search via [Serper.dev](https://serper.dev/)
- 🧠 Powered by Groq's blazing-fast LLaMA 3.3 70B model
- 🤖 Modular agent design using [Agno AI](https://github.com/agnodice/agno)
- 🧰 MCP-compatible tool handling for search queries
- 📝 Structured markdown output with context-aware results
- 🔁 Interactive CLI loop with session memory

---

## 📆 Requirements

- Python 3.8+
- `httpx`
- `python-dotenv`
- `agno` framework (including Groq + MCP tools)

Install dependencies:

```bash
pip install httpx python-dotenv agno
```

---

## 🔐 Environment Variables

Create a `.env` file in the root of your project:

```dotenv
GROQ_API_KEY=your_groq_api_key
SERPER_API_KEY=your_serper_api_key
```

---

## 🧠 How It Works

- A custom `PythonMCPServer` sends search queries to Serper.dev.
- Responses are parsed and formatted in MCP-compatible structure.
- A fake MCP session simulates actual plugin behavior.
- The `Agent` (Groq LLaMA 3-70B) calls `mcp_search` and formats answers using markdown and multiple sources.

---

## 🛠️ Usage

Start the agent from the command line:

```bash
python web_agent.py
```

You’ll be prompted for a query:

```bash
Enter your search query (type 'exit' or 'quit' to stop):
```

To stop the agent, type `exit` or `quit`.

---

## 📁 Project Structure

```bash
.
├── web_agent.py              # Main script with the search agent logic
├── .env                 # API keys (not committed)
└── README.md            # You're here!
```

---

## 🔗 Example Output

```markdown
## 🔎 Search Results for: "Latest news on AI in finance"

1. **AI is transforming the finance industry**  
   *"A recent report details how machine learning is improving fraud detection and portfolio optimization."*  
   ➤ [source](https://example.com/ai-in-finance) — *Serper/Google*

2. **Banks adopt generative AI tools**  
   *"JP Morgan and Goldman Sachs are integrating GenAI for client communication."*  
   ➤ [source](https://example.com/genai-banking) — *Serper/Google*
```

---

## 🙌 Acknowledgements

- [Groq](https://groq.com/)
- [Agno AI Framework](https://github.com/agnodice/agno)
- [Serper.dev](https://serper.dev/)

