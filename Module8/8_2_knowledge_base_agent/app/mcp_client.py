import json
import sys

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from mcp import types


async def search_documents_with_mcp(question: str) -> str:
    # Configure how to start MCP server.
    server_params = StdioServerParameters(
        command=sys.executable,
        args=["mcp_server.py"],
    )

    # Start MCP server and connect to it.
    async with stdio_client(server_params) as (read, write):

        # Create MCP session.
        async with ClientSession(read, write) as session:

            # Initialize MCP session.
            await session.initialize()

            # Call MCP tool.
            result = await session.call_tool(
                "search_company_knowledge_base",
                {
                    "question": question,
                },
            )

            # Extract text result.
            for content in result.content:
                if isinstance(content, types.TextContent):
                    return content.text

    # Fallback if tool returns nothing.
    return json.dumps(
        {
            "status": "error",
            "reason": "No MCP response returned.",
            "chunks": [],
        }
    )