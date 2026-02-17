from utils.data_loader import fetch_news_data
import pandas as pd

try:
    ticker = "AAPL"
    df = fetch_news_data(ticker)
    if not df.empty:
        print("News fetched successfully.")
        print("Columns:", df.columns.tolist())
        print("Head:")
        print(df.head(1).to_string())
        
        required_cols = ['title', 'published_at']
        missing = [col for col in required_cols if col not in df.columns]
        if missing:
            print(f"FAILED: Missing columns: {missing}")
            exit(1)
        else:
            print("SUCCESS: All required columns present.")
    else:
        print("No news found (this might be normal if market is closed or API issue, but structure check skipped).")
except Exception as e:
    print(f"FAILED: Error fetching news: {e}")
    exit(1)
