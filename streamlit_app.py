import streamlit as st
import requests
import json

# Streamlit app configuration
st.set_page_config(page_title="Sentiment Analysis App", page_icon="😊")

def analyze_text(text):
    """Send text to the Flask API and get sentiment analysis."""
    try:
        response = requests.post(
            'http://localhost:5000/analyze',
            json={'text': text},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {'error': f"Failed to connect to API: {str(e)}"}

# Streamlit UI
st.title("Sentiment Analysis Application")
st.markdown("Enter text below to analyze its sentiment using a pre-trained transformer model.")

# Text input
text_input = st.text_area("Input Text", placeholder="Type or paste your text here...", height=200)

# Analyze button
if st.button("Analyze Sentiment"):
    if text_input.strip():
        with st.spinner("Analyzing..."):
            result = analyze_text(text_input)
        
        if 'error' in result:
            st.error(result['error'])
        else:
            st.subheader("Analysis Results")
            st.write(f"**Original Text**: {result['text']}")
            st.write(f"**Processed Text**: {result['processed_text']}")
            st.write(f"**Sentiment**: {result['sentiment']}")
            st.write(f"**Confidence**: {result['confidence']:.4f}")
            
            # Display sentiment with emoji
            if result['sentiment'] == 'POSITIVE':
                st.success("😊 Positive sentiment detected!")
            else:
                st.warning("😔 Negative sentiment detected!")
    else:
        st.error("Please enter some text to analyze.")

# Footer
st.markdown("---")
st.markdown("Built with Streamlit and powered by a Flask API with Hugging Face's DistilBERT model.")