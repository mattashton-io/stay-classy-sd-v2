from fastmcp.client import Client
import asyncio
from fastmcp.client.transports import StreamableHttpTransport


async def main():
    async with Client(StreamableHttpTransport(url="http://127.0.0.1:8000/mcp")) as client:
        await client.ping()
        result = await client.call_tool("test_func")
        print(result)

asyncio.run(main())