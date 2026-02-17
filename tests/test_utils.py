import unittest
import pandas as pd
from utils.sentiment_analyzer import analyze_sentiment, process_news_sentiment

class TestSentimentAnalyzer(unittest.TestCase):
    def test_analyze_sentiment(self):
        text = "This is a great stock!"
        score = analyze_sentiment(text)
        self.assertTrue(score > 0)
        
        text = "This is a terrible loss."
        score = analyze_sentiment(text)
        self.assertTrue(score < 0)

    def test_process_news_sentiment(self):
        data = {'title': ["Good news", "Bad news", "Neutral statement"]}
        df = pd.DataFrame(data)
        processed_df = process_news_sentiment(df)
        self.assertIn('sentiment_score', processed_df.columns)
        self.assertIn('sentiment_label', processed_df.columns)
        self.assertEqual(processed_df.iloc[0]['sentiment_label'], 'Positive')
        self.assertEqual(processed_df.iloc[1]['sentiment_label'], 'Negative')

if __name__ == '__main__':
    unittest.main()
