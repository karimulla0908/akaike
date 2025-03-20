import streamlit as st
import requests

st.title("News Summarization & Sentiment Analysis")

company = st.text_input("Enter Company Name")

if st.button("Get News"):
    response = requests.get(f"http://0.0.0.0:8000/get_news/?company={company}")
    
    if response.status_code == 200:
        data = response.json()
        st.write("### Sentiment Report")
        st.json(data["Sentiment Report"])
        
        st.write("### News Articles")
        for article in data["Articles"]:
            st.subheader(article["title"])
            st.write(f"**Summary:** {article['summary']}")
            st.write(f"**Sentiment:** {article['Sentiment']}")
        
        # Display Final Sentiment Summary
        st.write("## Final Sentiment Analysis")
        st.write(f"**{data['Sentiment Report']['Final Sentiment Analysis']}**")

        # Display Final Sentiment Summary in Hindi
        st.write("## अंतिम भावना विश्लेषण (Final Sentiment Analysis in Hindi)")
        st.write(f"**{data['Sentiment Report']['Final Sentiment Analysis Hindi']}**")

        # Play Hindi Speech
        st.write("## हिंदी ऑडियो (Hindi Audio)")
        if data["Audio"] != "TTS Generation Failed":
            st.audio("output_hindi.mp3")
        else:
            st.write("Text-to-Speech generation failed.")
    else:
        st.error("Error fetching data")
