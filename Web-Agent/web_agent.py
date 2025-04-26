import asyncio
import os
import httpx
from dotenv import load_dotenv
from agno.agent import Agent
from agno.tools.mcp import MCPTools
from agno.models.groq import Groq
from loguru import logger

# Load environment variables
load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Setup logger
logger.add("web_agent.log", format="{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}", rotation="5 MB", level="DEBUG")
logger.info("==== MCP Web Agent Started ====")


class PythonMCPServer:
    def __init__(self):
        self.base_url = "https://google.serper.dev"
        self.headers = {
            "X-API-KEY": os.getenv("SERPER_API_KEY"),
            "Content-Type": "application/json"
        }

    async def execute(self, command: dict):
        try:
            if command["action"] == "search":
                logger.debug(f"Executing search for query: {command['query']}")
                return await self._handle_search(command["query"])
            logger.warning(f"Unsupported action received: {command['action']}")
            return {"error": "Unsupported MCP action"}
        except Exception as e:
            logger.error(f"Error during MCP execution: {e}")
            return {"error": str(e)}

    async def _handle_search(self, query: str):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/search",
                    headers=self.headers,
                    json={"q": query, "num": 5}
                )
                response.raise_for_status()
                return self._format_mcp_response(response.json())
        except Exception as e:
            logger.error(f"Search request failed for query '{query}': {e}")
            return {"error": f"Search failed: {str(e)}"}

    def _format_mcp_response(self, data: dict):
        logger.debug("Formatting MCP response")
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
    try:
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

        logger.info(f"Running query: {query}")
        await agent.aprint_response(query, stream=True)
    except Exception as e:
        logger.error(f"Failed to run agent for query '{query}': {e}")


if __name__ == "__main__":
    try:
        while True:
            user_query = input("Enter your search query (type 'exit' or 'quit' to stop): ")
            if user_query.strip().lower() in {"exit", "quit"}:
                logger.info("User exited the MCP Agent.")
                print("Exiting MCP Agent.")
                break
            asyncio.run(run_agent(user_query))
    except KeyboardInterrupt:
        logger.warning("User interrupted execution with keyboard.")
        print("\nInterrupted. Exiting MCP Agent.")
    except Exception as e:
        logger.critical(f"Unexpected error in main loop: {e}")
