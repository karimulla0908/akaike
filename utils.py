import requests
from bs4 import BeautifulSoup
from nltk.sentiment import SentimentIntensityAnalyzer
import nltk
import pandas as pd
from gtts import gTTS
import os

# Download necessary NLTK resources
nltk.download('vader_lexicon')
sia = SentimentIntensityAnalyzer()

def get_news_urls(company_name):
    """Fetch news articles using SerpAPI instead of Google scraping."""
    API_KEY = "d5872201b114296c84fc519d10284e7bc4ad8bcf52249ef49904fe3e85c990be"  # Replace with your actual key
    url = "https://serpapi.com/search"

    params = {
        "q": f"{company_name} news",
        "tbm": "nws",
        "api_key": API_KEY
    }

    response = requests.get(url, params=params)
    data = response.json()

    if "news_results" in data:
        article_urls = [result["link"] for result in data["news_results"]][:10]
        return article_urls
    else:
        return []  # Return empty list if no articles found

def extract_article_details(url):
    """Extracts title and summary using BeautifulSoup instead of newspaper3k."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        title = soup.title.string if soup.title else "No Title"
        paragraphs = soup.find_all('p')
        text = " ".join([p.get_text() for p in paragraphs[:5]])

        if not text.strip():
            text = "No content available"

        return {
            "title": title,
            "summary": text,
            "text": text
        }
    except Exception:
        return {
            "title": "No Title",
            "summary": "No summary available",
            "text": "No content available"
        }

def analyze_sentiment(text):
    """Classifies sentiment as Positive, Neutral, or Negative."""
    if not text.strip():
        return "Neutral"  # Default to neutral if no text available

    score = sia.polarity_scores(text)['compound']
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

def compare_sentiments(articles, company):
    """Analyzes sentiment distribution, topic overlap, and generates a final sentiment summary."""
    sentiment_counts = {"Positive": 0, "Negative": 0, "Neutral": 0}
    topics = []
    
    for article in articles:
        if "Sentiment" in article:
            sentiment_counts[article["Sentiment"]] += 1
        
        if "summary" in article:
            topics.extend(article["summary"].split())

    common_topics = set(topics)

    # Generate a Final Sentiment Summary in English
    max_sentiment = max(sentiment_counts, key=sentiment_counts.get)
    if max_sentiment == "Positive":
        final_summary = f"{company}'s latest news coverage is mostly positive. Potential stock growth expected."
    elif max_sentiment == "Negative":
        final_summary = f"{company} is facing negative coverage. Investors should be cautious."
    else:
        final_summary = f"{company} has mixed or neutral coverage with no strong impact on the market."

    # Generate Hindi summary
    hindi_summary = {
        "Positive": f"{company} की हालिया समाचार कवरेज सकारात्मक है। स्टॉक वृद्धि की संभावना है।",
        "Negative": f"{company} को नकारात्मक समाचार मिल रहा है। निवेशकों को सतर्क रहना चाहिए।",
        "Neutral": f"{company} की खबरें मिश्रित या तटस्थ हैं, कोई बड़ा प्रभाव नहीं।"
    }

    final_hindi_summary = hindi_summary[max_sentiment]

    return {
        "Sentiment Distribution": sentiment_counts,
        "Topic Overlap": list(common_topics),
        "Final Sentiment Analysis": final_summary,
        "Final Sentiment Analysis Hindi": final_hindi_summary
    }

def generate_tts(text, lang="hi"):
    """Converts text to Hindi speech and saves as an audio file."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        audio_file = "output_hindi.mp3"
        tts.save(audio_file)
        return audio_file if os.path.exists(audio_file) else None
    except Exception:
        return None  # Return None if TTS fails
