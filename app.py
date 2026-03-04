import streamlit as st
import requests

st.set_page_config(
    page_title="AI Student Mental Wellness System",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 AI-Based Student Mental Wellness Screening Tool")
st.markdown("Exam stress + lifestyle + symptom-based analysis")

text = st.text_area("✍️ Enter your thoughts about exams:", height=150)

sleep_hours = st.slider("😴 Sleep hours per day", 0, 12, 6)
study_hours = st.slider("📚 Study hours per day", 0, 12, 3)

st.markdown("### 🩺 Symptom Checklist")

appetite_change = st.checkbox("🍽️ Appetite changes")
headaches = st.checkbox("🤕 Frequent headaches or fatigue")
panic_symptoms = st.checkbox("😰 Panic or anxiety attacks")

if st.button("Analyze"):

    if text.strip() == "":
        st.warning("Please enter your thoughts first.")
    else:
        try:
            response = requests.post(
                "http://127.0.0.1:8000/predict",
                json={
                    "text": text,
                    "sleep_hours": float(sleep_hours),
                    "study_hours": float(study_hours),
                    "appetite_change": bool(appetite_change),
                    "headaches": bool(headaches),
                    "panic_symptoms": bool(panic_symptoms)
                }
            )

            if response.status_code != 200:
                st.error(f"Backend Error: {response.text}")
            else:
                result = response.json()

                anxiety_level = result["anxiety_level"]
                confidence = result["confidence"]
                suggestion = result["suggestion"]
                final_status = result["final_status"]
                risk_score = result["risk_score"]
                label = result["label"]
                recommendation = result["recommendation"]

                st.markdown("---")
                st.subheader("📊 Anxiety Analysis")

                if anxiety_level == "High":
                    st.error(f"🔴 Anxiety Level: {anxiety_level}")
                elif anxiety_level == "Moderate":
                    st.warning(f"🟡 Anxiety Level: {anxiety_level}")
                else:
                    st.success(f"🟢 Anxiety Level: {anxiety_level}")

                st.progress(int(confidence * 100))
                st.markdown(f"Confidence Score: {round(confidence * 100, 1)}%")
                st.markdown(f"Model Sentiment: {label}")

                st.markdown("---")
                st.subheader("🧠 Overall Mental Health Assessment")

                if final_status == "High Mental Health Risk":
                    st.error(f"🔴 {final_status}")
                elif final_status == "Moderate Risk":
                    st.warning(f"🟡 {final_status}")
                else:
                    st.success(f"🟢 {final_status}")

                st.markdown(f"Risk Score: {risk_score}")
                st.info(f"💡 AI Suggestion: {suggestion}")

                st.markdown("### 🏥 Personalized Recommendation")
                st.write(recommendation)

        except Exception as e:
            st.error(f"Connection Error: {e}")

st.markdown("---")
st.caption("⚠️ Educational screening tool only. Not a medical diagnosis system.")