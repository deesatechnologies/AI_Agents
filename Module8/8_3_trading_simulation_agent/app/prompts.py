def build_trading_prompt(
    stock_symbol: str,
    market_data: dict,
):
    # Prompt for trading analysis.
    return f"""
You are a cautious AI trading assistant.

Analyze the following market data and provide a trading recommendation.

Stock Symbol:
{stock_symbol}

Market Data:
{market_data}

Rules:
- Never guarantee profits.
- Mention risks clearly.
- Keep recommendation conservative.
- Use only the provided market data.
- Final recommendation should be:
  BUY
  HOLD
  or SELL

Explain reasoning clearly.
"""