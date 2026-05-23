import yfinance as yf


def get_market_data(stock_symbol: str):
    # Wrap everything in try/except
    # so app does not crash if internet/API fails.
    try:

        # Convert stock symbol to uppercase.
        stock_symbol = stock_symbol.upper()

        # Create Yahoo Finance ticker object.
        ticker = yf.Ticker(stock_symbol)

        # Fetch last 2 days of stock history.
        history = ticker.history(period="2d")

        # Handle invalid or missing stock symbols.
        if history.empty:
            return None

        # Latest closing stock price.
        latest_close = round(
            history["Close"].iloc[-1],
            2,
        )

        # Previous day's closing price.
        previous_close = round(
            history["Close"].iloc[-2],
            2,
        )

        # Calculate daily percentage movement.
        daily_change_percent = round(
            (
                (latest_close - previous_close)
                / previous_close
            ) * 100,
            2,
        )

        # Get latest trading volume.
        volume = int(
            history["Volume"].iloc[-1]
        )

        # Determine volatility category.
        volatility = (
            "HIGH"
            if abs(daily_change_percent) > 3
            else "LOW"
        )

        # Return formatted market data.
        return {
            "price": latest_close,
            "daily_change_percent": daily_change_percent,
            "volume": volume,
            "volatility": volatility,
        }

    except Exception as error:
        # Print error in terminal for debugging.
        print("\n=== MARKET DATA ERROR ===")
        print(error)
        print("=========================\n")

        # Return None so app handles failure safely.
        return None