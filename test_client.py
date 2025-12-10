from fastmcp.client import Client
import asyncio
from fastmcp.client.transports import StreamableHttpTransport


async def main():
    async with Client(StreamableHttpTransport(url="http://127.0.0.1:8000/mcp")) as client:
        await client.ping()
        # Test basic function
        result_func = await client.call_tool("test_func")
        print(f"Test Func Result: {result_func}")
        
        # Test weather function
        print("\nTesting Weather Tool...")
        result_weather = await client.call_tool("get_weather", arguments={"location": "San Diego, CA"})
        print(f"Weather Result: {result_weather}")

asyncio.run(main())
