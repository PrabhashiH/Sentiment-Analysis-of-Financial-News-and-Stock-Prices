import plotly.graph_objs as go
import plotly.express as px
from plotly.subplots import make_subplots

def plot_stock_price(stock_df, ticker):
    """
    Plots the stock closing price over time.
    """
    if stock_df.empty:
        return None
    
    fig = px.line(stock_df, x=stock_df.index, y='Close', title=f'{ticker} Stock Price')
    return fig

def plot_sentiment_trend(news_df):
    """
    Plots the sentiment trend over time.
    """
    if news_df.empty or 'published_at' not in news_df.columns:
        return None
    
    # Aggregate sentiment by date (if multiple articles per day) - for simplicity, we plot individual points first
    # Or cleaner: scatter plot
    fig = px.scatter(news_df, x='published_at', y='sentiment_score', 
                     color='sentiment_label',
                     title='News Sentiment Over Time',
                     labels={'sentiment_score': 'Sentiment Score', 'published_at': 'Date'},
                     hover_data=['title'])
    return fig

def plot_correlation(stock_df, news_df):
    """
    Plots stock price and sentiment on the same chart with dual axes.
    Note: This requires aligning dates. 
    Since news is sparse, we might just overlay them.
    """
    if stock_df.empty or news_df.empty:
        return None

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    # Add stock price
    fig.add_trace(
        go.Scatter(x=stock_df.index, y=stock_df['Close'], name="Stock Price", mode='lines'),
        secondary_y=False,
    )

    # Add sentiment
    # We might want to resample stock data to match news or vice versa, 
    # but for a simple visual, just plotting points is fine.
    fig.add_trace(
        go.Scatter(x=news_df['published_at'], y=news_df['sentiment_score'], name="Sentiment", mode='markers',
                   marker=dict(size=10, color=news_df['sentiment_score'], colorscale='RdYlGn', showscale=True)),
        secondary_y=True,
    )

    fig.update_layout(
        title_text="Stock Price vs News Sentiment"
    )

    fig.update_yaxes(title_text="Stock Price", secondary_y=False)
    fig.update_yaxes(title_text="Sentiment Score", secondary_y=True)

    return fig
