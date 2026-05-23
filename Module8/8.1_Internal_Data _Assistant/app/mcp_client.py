import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import types

#This code:Start the MCP server by running mcp_server.py using the current Python interpreter
async def call_internal_data_tool(sql_query: str) -> str:
    # Configure how to start the MCP server.
    #StdioServerParameters is a class for taking input parameters needed to start and communicate
    #with an MCP Server using stdio transport
    server_params = StdioServerParameters(
        command=sys.executable, #use the current Python interpreter
        args=["mcp_server.py"]
    )

    # Start server process and connect through stdio.
    async with stdio_client(server_params) as (read, write):

        # Create MCP client session.
        async with ClientSession(read, write) as session:

            # Initialize MCP session.
            await session.initialize()

            # Call MCP tool with SQL query.  call_tool :“Execute a tool exposed by MCP server.”
            result = await session.call_tool(
                "query_internal_sales_data", #tool name that we exposed using @mcp.tool
                {
                    "sql_query": sql_query,
                }
            )

            # Extract text content from MCP result.
            for content in result.content:
                if isinstance(content, types.TextContent):
                    return content.text

    # Fallback response if no text content returned.
    return json.dumps(
        {
            "status": "error",
            "reason": "No MCP tool response returned.",
            "data": [],
        }
    )