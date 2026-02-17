import yfinance as yf
import json

try:
    ticker = "AAPL"
    stock = yf.Ticker(ticker)
    news = stock.news
    if news:
        with open("news_debug.json", "w") as f:
            # Dump the first item completely
            json.dump(news[0], f, indent=2)
        print("Dumped news to news_debug.json")
    else:
        print("No news found.")
except Exception as e:
    print(f"Error: {e}")
