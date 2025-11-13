import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from app.clients.mcp.load_tools import create_graph

# Define server parameters (adjust the path to your server script)
server_params = StdioServerParameters(
    command="python",
    args=["wikipedia_server.py"]
)


# We define the asynchronous entry point function main(), which coordinates the MCP connection and user interaction loop.
async def main():
    # stdio_client is a LangChain-compatible client that connects to the MCP server over standard input/output. It
    # handles the low-level communication channel.
    # We use stdio_client(server_params) to launch the MCP server as a subprocess and open standard input/output streams
    # (read, write) for communication
    async with stdio_client(server_params) as (read, write):
        # We create a ClientSession using the I/O streams. This manages the life cycle of the client’s interaction with
        # the server.
        async with ClientSession(read, write) as session:
            # We call session.initialize() to complete the initial handshake and prepare for tool discovery and
            # execution.
            await session.initialize()

            # We call create_graph(session) to compile the LangGraph-based agent using the initialized client session.
            agent = await create_graph(session)

            print("Wikipedia MCP Agent is ready")

            while True:
                user_input = input("\n You: ").strip()

                if user_input.lower() in {"exit", "quit", "q"}:
                    break

                try:
                    # We call agent.ainvoke(...) to send the user's message into the graph.
                    # - The message is passed via the "messages" field of the state.
                    # - We provide a thread identifier using config={"configurable": {"thread_id": "wiki-session"}} to
                    # scope the state tracking.
                    response = await agent.aiinvoke(
                        {"message": user_input},
                        config={"configurable": {"thread_id": "wiki_session"}}
                    )
                    # We extract the final message from the response and print the assistant’s reply.
                    print("AI:", response["messages"][-1]["content"])
                except Exception as e:
                    print("Error:", str(e))


# Run the asynchronous function
if __name__ == "__main__":
    asyncio.run(main())