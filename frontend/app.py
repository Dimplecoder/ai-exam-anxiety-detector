import streamlit as st
import requests

BACKEND_URL = "https://your-render-url.onrender.com/predict"

st.title("🧠 AI Exam Anxiety Detector")

text = st.text_area("Enter your thoughts about exams:")

if st.button("Analyze"):
    if text:
        response = requests.post(
            BACKEND_URL,
            json={"text": text}
        )

        if response.status_code == 200:
            result = response.json()
            st.success(f"Anxiety Level: {result['anxiety_level']}")
            st.write(f"Confidence: {result['confidence']}")
        else:
            st.error("Backend Error")