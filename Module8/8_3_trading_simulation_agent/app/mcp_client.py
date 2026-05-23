import sys

from mcp import ClientSession
from mcp import StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import types


async def fetch_market_data(stock_symbol: str):
    # Configure how to start MCP server.
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
    )

    # Start MCP server connection.
    async with stdio_client(
        server_params
    ) as (read, write):

        # Create MCP session.
        async with ClientSession(
            read,
            write,
        ) as session:

            # Initialize session.
            await session.initialize()

            # Call MCP tool.
            result = await session.call_tool(
                "get_stock_market_data",
                {
                    "stock_symbol": stock_symbol,
                },
            )

            # Extract tool text response.
            for content in result.content:
                if isinstance(
                    content,
                    types.TextContent,
                ):
                    return content.text

    return None