import streamlit as st
import requests
import streamlit_placeholder

st.title("News Bias Tracker")
st.text("Paste in the URL of a news article you want analyzed here")
url = st.text_input("URL:")

if st.button("Analyze"):
    if url.strip() == "":
        st.warning("Please enter a valid URL.")
    else:
        with st.spinner("Analyzing...this may take a while"):
            polarity, std, result = streamlit_placeholder.run_program(url)
    st.success("analysis complete")
    st.write("article polarity:", polarity)
    st.write("polarity standard deviation:", std)
    st.write("results:", result)