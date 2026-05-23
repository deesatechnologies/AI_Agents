# High-risk volatility threshold.
MAX_ALLOWED_DAILY_CHANGE = 5


# Blocked high-risk stocks.
BLOCKED_STOCKS = [
    "GAMBLINGCOIN",
    "MEMESTOCK",
]


def validate_stock_request(stock_symbol: str):
    # Convert stock symbol to uppercase.
    stock_symbol = stock_symbol.upper()

    # Block risky or fake assets.
    if stock_symbol in BLOCKED_STOCKS:
        return False, "Trading blocked for high-risk asset."

    return True, "Stock request allowed."


def validate_market_risk(market_data: dict):
    # Extract daily movement percentage.
    daily_change = abs(
        market_data["daily_change_percent"]
    )

    # Block extreme market movement.
    if daily_change > MAX_ALLOWED_DAILY_CHANGE:
        return False, (
            "Trade blocked due to excessive market volatility."
        )

    return True, "Risk check passed."


def validate_final_recommendation(answer: str):
    # Convert answer to lowercase.
    lower_answer = answer.lower()

    # Block dangerous financial advice.
    blocked_phrases = [
        "guaranteed profit",
        "risk-free",
        "all in",
        "100% safe",
    ]

    # Check for dangerous wording.
    for phrase in blocked_phrases:
        if phrase in lower_answer:
            return False, (
                f"Unsafe financial recommendation detected: {phrase}"
            )

    return True, "Recommendation approved."