import streamlit as st
import requests
import altair as alt
import pandas as pd

st.title("Sentiment Analysis Dashboard")
text = st.text_area("Enter text for analysis")
token = st.text_input("Enter JWT Token", type="password")
api_key = st.text_input("Enter API Key")

if st.button("Analyze"):
    headers = {"Authorization": f"Bearer {token}", "X-API-Key": api_key}
    response = requests.post("http://api-gateway:8000/analyze/analyze", json={"text": text}, headers=headers)
    if response.status_code == 200:
        result = response.json()
        st.write(f"Sentiment: {result['sentiment']} (Score: {result['score']:.2f})")
        requests.post("http://api-gateway:8000/store/store", json={"user_id": "1", "text": text, "sentiment": result["sentiment"]}, headers=headers)
        df = pd.DataFrame({"Text": [text], "Sentiment": [result["sentiment"]], "Score": [result["score"]]})
        chart = alt.Chart(df).mark_bar().encode(x="Sentiment", y="Score")
        st.altair_chart(chart, use_container_width=True)
    else:
        st.error(response.json().get("error", "Analysis failed"))