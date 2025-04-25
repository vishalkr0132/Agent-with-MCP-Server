import asyncio
import os
import httpx
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.models.groq import Groq

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

class PythonMCPServer:
    def __init__(self):
        self.base_url = "https://google.serper.dev"
        self.headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json"
        }

    async def execute(self, command: dict):
        if command["action"] == "search":
            return await self._handle_search(command["query"])
        return {"error": "Unsupported MCP action"}

    async def _handle_search(self, query: str):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/search",
                headers=self.headers,
                json={"q": query, "num": 5}
            )
            return self._format_mcp_response(response.json())

    def _format_mcp_response(self, data: dict):
        return {
            "mcp_version": "1.0",
            "results": [
                {
                    "title": item.get("title"),
                    "url": item.get("link"),
                    "content": item.get("snippet"),
                    "source": "Serper/Google"
                }
                for item in data.get("organic", [])
            ]
        }


class FakeMCPSession:
    def __init__(self, server: PythonMCPServer):
        self.server = server

    async def execute(self, command: dict):
        return await self.server.execute(command)


async def run_agent(query: str):
    server = PythonMCPServer()
    session = FakeMCPSession(server=server)
    mcp_tools = MCPTools(session=session)

    agent = Agent(
        name="Web Agent",
        role="Search the web for information",
        model=Groq(id="llama-3.3-70b-versatile"),
        tools=[mcp_tools],
        instructions="""\
        MCP Research Protocol:
        1. Use mcp_search for all queries
        2. Validate across multiple results
        3. Format with MCP-standard markdown
        4. Include source metadata
        5. Maintain session context""",
        markdown=True,
        show_tool_calls=True
    )
    await agent.aprint_response(query, stream=True)


if __name__ == "__main__":
    while True:
        user_query = input("Enter your search query (type 'exit' or 'quit' to stop): ")
        if user_query.strip().lower() in {"exit", "quit"}:
            print("Exiting MCP Agent.")
            break
        asyncio.run(run_agent(user_query))
