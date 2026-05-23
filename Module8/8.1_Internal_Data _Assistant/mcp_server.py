import json

from mcp.server.fastmcp import FastMCP

from app.database import (
    create_demo_database,
    run_read_only_query
)

from app.guardrails import (
    validate_sql_query
)


# Create MCP server.
mcp = FastMCP("internal-data-server")


@mcp.tool()
def query_internal_sales_data(sql_query: str) -> str:
    # This function is exposed as an MCP tool.
    # The AI assistant can call this tool through the MCP client.

    # Validate SQL before executing.
    is_allowed, message = validate_sql_query(sql_query)

    # If SQL violates guardrails, block it.
    if not is_allowed:
        return json.dumps(
            {
                "status": "blocked",
                "reason": message,
                "data": [],
            }
        )

    try:
        # Execute safe read-only SQL.
        results = run_read_only_query(sql_query)

        # Return structured JSON string.
        return json.dumps(
            {
                "status": "success",
                "reason": "Query executed successfully.",
                "data": results
            },
            indent=2
        )

    except Exception as error:
        # Return safe error message.
        return json.dumps(
            {
                "status": "error",
                "reason": str(error),
                "data": []
            }
        )


if __name__ == "__main__":
    # Create demo database when MCP server starts.
    create_demo_database()

    # Start MCP server using STDIO transport.
    mcp.run()