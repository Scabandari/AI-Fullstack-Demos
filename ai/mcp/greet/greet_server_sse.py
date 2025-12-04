from mcp.server.fastmcp import FastMCP
from fastapi import FastAPI

app = FastAPI()
mcp = FastMCP("Server to manage a Linux instance")


@mcp.tool
def greet(name: str) -> str:
    return f"Hello, {name}!"


app.mount("/", mcp.sse_app())
