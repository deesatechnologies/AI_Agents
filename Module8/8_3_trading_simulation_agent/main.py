import json

import gradio as gr

from app.llm_service import call_llm

from app.prompts import (
    build_trading_prompt,
)

from app.mcp_client import (
    fetch_market_data,
)

from app.guardrails import (
    validate_final_recommendation,
)


async def run_trading_simulation(
    stock_symbol: str,
):
    # Validate empty stock symbol.
    if not stock_symbol or not stock_symbol.strip():
        return "Please enter a stock symbol."

    # Fetch live market data using MCP tool.
    tool_result = await fetch_market_data(
        stock_symbol
    )

    # Handle empty MCP response.
    if not tool_result:
        return """
                # MCP Tool Error

                    No response received from MCP server.
                """

    # Parse MCP JSON response.
    try:
        parsed_result = json.loads(tool_result)

    except Exception as error:
        return f"""
                    # JSON Parsing Error

                    Error: {error}

                Raw Tool Result: {tool_result}
                """

    # Handle blocked trades.
    if parsed_result["status"] == "blocked":
        return f"""
                # Trade Blocked

                ## Reason {parsed_result["reason"]}
                ## Tool Result
                ```json
                {json.dumps(parsed_result, indent=2)}
                """

    # Handle API failure or invalid stock symbol.
    if parsed_result["status"] == "error":
        return f"""
                     Market Data Error
                        Reason {parsed_result["reason"]}
                """


    # Extract safe market data.
    market_data = parsed_result["market_data"]

    # Build AI trading analysis prompt.
    prompt = build_trading_prompt(
        stock_symbol,
        market_data,
        )

    # System prompt for safe financial assistant.
    system_prompt = (
        "You are a cautious financial assistant. "
        "Never guarantee profits or risk-free investing."
        )

    # Call LLM to generate recommendation.
    recommendation = call_llm(
        system_prompt=system_prompt,
        user_prompt=prompt,
        )

    # Validate final recommendation.
    allowed, message = (
        validate_final_recommendation(
        recommendation
        )
        )

    # Block unsafe AI recommendations.
    if not allowed:
        return f"""
        Reason  {message} """

    # Return transparent workflow result.
    return f"""
        Trading Simulation Result
        Stock Symbol
        {stock_symbol.upper()}
        Live Market Data
        {json.dumps(market_data, indent=2)}
        AI Recommendation
        {recommendation}
        """

#UI with gradio
with gr.Blocks() as demo:
    # Application title.
    gr.Markdown(
        "# Trading Simulation Agent — MCP + Guardrails"
        )

    # Application description.
    gr.Markdown(
        "AI trading simulation using live stock market data, "
        "MCP tools, and enterprise risk guardrails."
        )

    # Stock symbol input.
    stock_input = gr.Textbox(
        label="Stock Symbol",
        placeholder="Examples: AAPL, TSLA, NVDA, MSFT",
        )

    # Run simulation button.
    run_button = gr.Button(
        "Run Trading Simulation"
        )

    # Final output display.
    output = gr.Markdown()

    # Button click event.
    run_button.click(
        fn=run_trading_simulation,
        inputs=stock_input,
        outputs=output,
    )

# =====================================================
# Main
# =====================================================

if __name__ == "__main__":
    demo.launch()
