import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta

def fetch_stock_data(ticker, start_date, end_date):
    """
    Fetches historical stock data using yfinance.
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date)
        return df
    except Exception as e:
        print(f"Error fetching stock data: {e}")
        return pd.DataFrame()

def fetch_news_data(ticker):
    """
    Fetches recent news for a given ticker using yfinance.
    Returns a DataFrame with columns: ['title', 'publisher', 'link', 'published_at']
    """
    try:
        stock = yf.Ticker(ticker)
        news = stock.news
        if news:
            news_data = []
            for item in news:
                if not isinstance(item, dict):
                    continue
                content = item.get('content', {})
                if not isinstance(content, dict):
                    continue
                
                news_entry = {
                    'title': content.get('title'),
                    'publisher': (content.get('provider') or {}).get('displayName'),
                    'link': (content.get('clickThroughUrl') or {}).get('url'),
                    'pubDate': content.get('pubDate'),
                    'summary': content.get('summary')
                }
                news_data.append(news_entry)
            
            if not news_data:
                return pd.DataFrame()

            df = pd.DataFrame(news_data)
            
            # Convert timestamp to datetime
            if 'pubDate' in df.columns:
                 df['published_at'] = pd.to_datetime(df['pubDate'])
            
            return df
        else:
            return pd.DataFrame()
    except Exception as e:
        print(f"!!! ERROR !!!: {e}")
        return pd.DataFrame()
