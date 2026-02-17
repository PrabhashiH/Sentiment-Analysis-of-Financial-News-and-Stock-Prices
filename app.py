import streamlit as st
import pandas as pd
from datetime import datetime, timedelta


from utils.data_loader import fetch_stock_data, fetch_news_data
from utils.sentiment_analyzer import process_news_sentiment, analyze_sentiment
from utils.visualizer import plot_stock_price, plot_sentiment_trend, plot_correlation

st.set_page_config(page_title="Stock Sentiment Analysis", layout="wide")

st.title("Financial News Sentiment & Stock Price Analysis")

# Sidebar for user input
st.sidebar.header("Configuration")
ticker = st.sidebar.text_input("Enter Stock Ticker", value="AAPL").upper()
days_to_look_back = st.sidebar.slider("Days to Look Back", min_value=7, max_value=365, value=30)
start_date = (datetime.now() - timedelta(days=days_to_look_back)).strftime('%Y-%m-%d')
end_date = datetime.now().strftime('%Y-%m-%d')

if st.sidebar.button("Analyze"):
    with st.spinner(f"Fetching data for {ticker}..."):
        # 1. Fetch Stock Data
        stock_df = fetch_stock_data(ticker, start_date, end_date)
        
        # 2. Fetch News Data
        news_df = fetch_news_data(ticker)
        
        if stock_df.empty:
            st.error(f"No stock data found for {ticker}.")
        else:
            st.success(f"Loaded stock data for {ticker}.")
            
            # Display Stock Price
            st.subheader(f"{ticker} Stock Price History")
            st.plotly_chart(plot_stock_price(stock_df, ticker), use_container_width=True)

            # 3. Analyze Sentiment
            if not news_df.empty:
                st.subheader(f"Recent News Sentiment for {ticker}")
                
                # Apply sentiment analysis
                news_df = process_news_sentiment(news_df)
                
                # Display processed news
                st.dataframe(
                    news_df[['published_at', 'title', 'publisher', 'sentiment_score', 'sentiment_label', 'link']].style.format({"link": lambda x: f'<a href="{x}" target="_blank">Link</a>'})
                    if 'link' in news_df.columns else news_df[['published_at', 'title', 'publisher', 'sentiment_score', 'sentiment_label']]
                )
                
                # Plot sentiment trend
                st.plotly_chart(plot_sentiment_trend(news_df), use_container_width=True)
                
                # 4. Correlation Analysis
                st.subheader("Correlation: Stock Price vs Sentiment")
                # Filter stock data to match news date range roughly for better visualization if needed
                # But for now, we just plot what we have.
                st.plotly_chart(plot_correlation(stock_df, news_df), use_container_width=True)
                
                # Calculate simple correlation if enough data points
                # This is tricky because news timestamps and stock dates don't align perfectly.
                # We'd need to aggregate daily sentiment and join with stock price.
                
                # Simple Daily Aggregation for Correlation
                news_df['date'] = news_df['published_at'].dt.date
                daily_sentiment = news_df.groupby('date')['sentiment_score'].mean().reset_index()
                daily_sentiment['date'] = pd.to_datetime(daily_sentiment['date']).dt.tz_localize(None) # Remove timezone for merge
                
                # Prepare stock data for merge
                stock_df_reset = stock_df.reset_index()
                stock_df_reset['date'] = pd.to_datetime(stock_df_reset['Date']).dt.tz_localize(None) # Remove timezone
                
                merged_df = pd.merge(stock_df_reset, daily_sentiment, on='date', how='inner')
                
                if not merged_df.empty and len(merged_df) > 2:
                    correlation = merged_df['Close'].corr(merged_df['sentiment_score'])
                    st.metric("Correlation (Price vs Sentiment)", f"{correlation:.4f}")
                else:
                    st.info("Not enough overlapping data points to calculate correlation.")

            else:
                st.warning("No recent news found to analyze sentiment.")

st.sidebar.markdown("---")
st.sidebar.markdown("Built with Streamlit & VADER")
