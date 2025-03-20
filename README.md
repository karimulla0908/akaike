# News Summarization and Text-to-Speech Application

## Overview
This application extracts key details from multiple news articles related to a given company, performs sentiment analysis, conducts a comparative analysis, and generates a text-to-speech (TTS) output in Hindi.

## Features
- Web scraping to fetch news articles
- Sentiment analysis on articles
- Comparative sentiment analysis
- Hindi text-to-speech conversion
- User interface via Streamlit
- API backend using FastAPI

## Installation
### 1. Clone the Repository
```bash
git clone <repository_url>
cd news_tts_project
```

### 2. Create Virtual Environment
```bash
python -m venv env
source env/bin/activate  # On Mac/Linux
env\Scripts\activate  # On Windows
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

## Running the Application
### 1. Start the FastAPI Backend
```bash
uvicorn api:app --reload
```

### 2. Start the Streamlit Frontend
```bash
streamlit run app.py
```

## Deployment
- The application can be deployed on **Hugging Face Spaces**.
- Update `app.py` to point to the deployed API endpoint.

## API Usage
### Endpoint: `/get_news/`
- **Method**: GET
- **Parameters**: `company` (string)
- **Response**:
```json
{
  "Company": "Tesla",
  "Articles": [
    {
      "title": "Tesla's New Model Breaks Sales Records",
      "summary": "Tesla's latest EV sees record sales in Q3...",
      "Sentiment": "Positive"
    }
  ],
  "Sentiment Report": {
    "Sentiment Distribution": {"Positive": 1, "Negative": 0, "Neutral": 0}
  },
  "Audio": "output.mp3"
}
```

## Assumptions & Limitations
- Google News scraping might be restricted for some regions.
- Sentiment analysis is based on NLTK’s Vader model.
- News article content might not always be fully extractable.

## Contributors
- **Your Name**
