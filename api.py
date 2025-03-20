from fastapi import FastAPI
from utils import get_news_urls, extract_article_details, analyze_sentiment, compare_sentiments, generate_tts

app = FastAPI()

@app.get("/get_news/")
def get_news(company: str):
    """Fetch and analyze news for a given company."""
    urls = get_news_urls(company)
    articles = []
    
    for url in urls:
        details = extract_article_details(url)
        if details:
            details["Sentiment"] = analyze_sentiment(details["text"])
            articles.append(details)
    
    sentiment_report = compare_sentiments(articles, company)

    # Generate Hindi TTS for Final Sentiment Summary
    tts_file = generate_tts(sentiment_report["Final Sentiment Analysis Hindi"], lang="hi")

    return {
        "Company": company,
        "Articles": articles,
        "Sentiment Report": sentiment_report,
        "Audio": "output_hindi.mp3" if tts_file else "TTS Generation Failed"
    }
