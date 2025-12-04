import asyncio
from fastmcp import Client

client = Client("http://localhost:8123/mcp")


async def call_tool(name: str):
    async with client:
        result = await client.call_tool("greet", {"name": name})
        print(result)


asyncio.run(call_tool("Ford"))

# fastmcp run greetserver.py:mcp --transport http --port 8123
