try:
    import streamlit
    import yfinance
    import pandas
    import nltk
    import plotly
    import requests
    import bs4
    import textblob
    print("All imports successful.")
except ImportError as e:
    print(f"Import failed: {e}")
    exit(1)

# Verify nltk download works (or check if it exists)
try:
    nltk.data.find('sentiment/vader_lexicon.zip')
    print("VADER lexicon found.")
except LookupError:
    print("VADER lexicon not found, attempting download.")
    try:
        nltk.download('vader_lexicon')
        print("VADER lexicon downloaded.")
    except Exception as e:
        print(f"Failed to download VADER lexicon: {e}")
        # Don't fail the verification if download fails (might be network), but note it.
