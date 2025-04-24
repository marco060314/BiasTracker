import streamlit as st
import requests
import streamlit_placeholder

def is_url_valid(url):
    try:
        response = requests.get(url, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False
    
st.title("News Bias Tracker")
st.text("Paste in the URL of a news article you want analyzed here")
url = st.text_input("URL:")

if st.button("Analyze"):
    if not is_url_valid(url):
        st.error("The URL is not reachable or doesn't return a valid response.")
    if url.strip() == "":
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Scraping..."):
            polarity, std, result = streamlit_placeholder.run_program(url)
    st.success("Analysis Complete")
    st.write("article polarity:", polarity)
    st.write("polarity standard deviation:", std)
    st.write("results:", result)