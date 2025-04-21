"""
Simple chat example using MCPAgent with built-in conversation memory.

This Example demonstrates how to use MCP with its built-in
conversation history capabilities for better contextual interactions.

Special thanks to https://github.com/microsoft/playwrit-mcp for the server.
"""
import os
import asyncio
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from mcp_use import MCPAgent, MCPClient

async def run_memory_chat():
    """Run a chat using MCPAgent's built-in conversation memory."""
    # Load environment variables for API Keys
    load_dotenv()
    os.environ['GROQ_API_KEY'] = os.getenv("GROQ_API_KEY")

    # Config file path
    config_file = "browser_mcp.json"

    print("Initializing Chat...")

    # Create MCP Client and agent with memory enabled
    client = MCPClient.from_config_file(config_file)
    llm = ChatGroq(model='qwen-qwq-32b')

    # Create agent with memory_enabled = True
    agent = MCPAgent(
        llm=llm,
        client=client,
        max_steps=15,
        memory_enabled=True,
    )

    print("\n====== Interactive MCP Chat ========")
    print("Type 'exit' or 'quit' to end the conversation")
    print("Type 'clear' to clear conversation history")
    print("=================================\n")

    try:
        # Main chat loop
        while True:
            # Get user input
            user_input = input("\nYou: ")

            # Check for exit command
            if user_input.lower() in ["exit", "quit"]:
                print("Ending Conversation...")
                break

            if user_input.lower() == "clear":
                agent.clear_conversation_history()
                print("Conversation history cleared")
                continue

            # Get response from agent
            print("\nAssistant: ", end="", flush=True)

            try:
                response = await agent.run(user_input)
                print(response)
            except Exception as e:
                print(f"\nError: {e}")

    finally:
        # Clean up
        if client and client.sessions:
            await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(run_memory_chat())
