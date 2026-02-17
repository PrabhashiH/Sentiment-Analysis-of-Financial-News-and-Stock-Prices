import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd

# Download VADER lexicon if not already present
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
except LookupError:
    nltk.download('vader_lexicon')

def analyze_sentiment(text):
    """
    Analyzes the sentiment of a text string using VADER.
    Returns a compound score.
    """
    sia = SentimentIntensityAnalyzer()
    sentiment = sia.polarity_scores(text)
    return sentiment['compound']

def process_news_sentiment(news_df):
    """
    Applies sentiment analysis to a DataFrame of news articles.
    Assumes the DataFrame has a 'title' column.
    Adds a 'sentiment_score' column.
    """
    if news_df.empty or 'title' not in news_df.columns:
        return news_df

    news_df['sentiment_score'] = news_df['title'].apply(analyze_sentiment)
    
    # Categorize sentiment
    def categorize(score):
        if score >= 0.05:
            return 'Positive'
        elif score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    news_df['sentiment_label'] = news_df['sentiment_score'].apply(categorize)
    return news_df
