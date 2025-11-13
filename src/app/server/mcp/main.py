from app.server.mcp.server import app


if __name__ == "__main__":
    print("Starting mcp_server server")
    app.run(transport="stdio")
