import streamlit as st
import requests
import time

st.title("News Summarization & Sentiment Analysis")

company = st.text_input("Enter Company Name")

if st.button("Get News"):
    with st.spinner("Connecting to API server..."):
        try:
            response = requests.get(f"http://0.0.0.0:8000/get_news/?company={company}", timeout=30)
            
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
                st.error(f"Error fetching data: HTTP {response.status_code}")
        except requests.exceptions.ConnectionError:
            st.error("Could not connect to the API server. Please make sure it's running at http://0.0.0.0:8000")
        except requests.exceptions.Timeout:
            st.error("Connection to API server timed out. The request might be taking too long to process.")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
