from fastmcp import FastMCP

mcp = FastMCP("test_mcp")

@mcp.tool("test_func")
def test_func():
    """Returns my favorite number"""
    return 4

mcp.run(transport="http")