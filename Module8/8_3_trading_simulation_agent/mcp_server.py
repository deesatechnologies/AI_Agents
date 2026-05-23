import json

from mcp.server.fastmcp import FastMCP

from app.market_data import get_market_data

from app.guardrails import (
    validate_stock_request,
    validate_market_risk,
)


# Create MCP server.
mcp = FastMCP("trading-simulation-server")


@mcp.tool()
def get_stock_market_data(stock_symbol: str) -> str:
    # Validate stock request.
    allowed, message = validate_stock_request(
        stock_symbol
    )

    # Block unsafe stocks.
    if not allowed:
        return json.dumps(
            {
                "status": "blocked",
                "reason": message,
            }
        )

    # Fetch market data.
    market_data = get_market_data(stock_symbol)

    # Handle missing stock symbol.
    if not market_data:
        return json.dumps(
            {
                "status": "not_found",
                "reason": "Stock symbol not found.",
            }
        )

    # Run market risk validation.
    risk_allowed, risk_message = (
        validate_market_risk(market_data)
    )

    # Block risky market conditions.
    if not risk_allowed:
        return json.dumps(
            {
                "status": "blocked",
                "reason": risk_message,
                "market_data": market_data,
            }
        )

    # Return safe market data.
    return json.dumps(
        {
            "status": "success",
            "market_data": market_data,
        },
        indent=2,
    )


if __name__ == "__main__":
    # Start MCP server.
    mcp.run()