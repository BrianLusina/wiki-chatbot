from mcp import ClientSession, StdioServerParameters

# Define server parameters (adjust the path to your server script)
server_params = StdioServerParameters(
    command="python",
    args=["wikipedia_server.py"]
)
