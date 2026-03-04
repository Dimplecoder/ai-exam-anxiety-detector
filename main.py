from fastapi import FastAPI
from pydantic import BaseModel
from model import predict_anxiety

app = FastAPI()

class TextInput(BaseModel):
    text: str
    sleep_hours: float
    study_hours: float
    appetite_change: bool
    headaches: bool
    panic_symptoms: bool

@app.get("/")
def home():
    return {"message": "AI Student Mental Wellness System Running"}

@app.post("/predict")
def predict(data: TextInput):

    model_result = predict_anxiety(data.text)

    anxiety_level = model_result["anxiety_level"]
    confidence = model_result["confidence"]
    suggestion = model_result["suggestion"]
    label = model_result["label"]

    risk_score = 0

    if data.sleep_hours < 6:
        risk_score += 1

    if data.study_hours < 2:
        risk_score += 1

    if anxiety_level == "High":
        risk_score += 2
    elif anxiety_level == "Moderate":
        risk_score += 1

    if data.appetite_change:
        risk_score += 1

    if data.headaches:
        risk_score += 1

    if data.panic_symptoms:
        risk_score += 1

    if risk_score >= 5:
        final_status = "High Mental Health Risk"
    elif risk_score >= 3:
        final_status = "Moderate Risk"
    else:
        final_status = "Low Risk"

    if final_status == "High Mental Health Risk":
        recommendation = "Consider consulting a counselor or healthcare professional. Improve sleep hygiene and structured planning."
    elif final_status == "Moderate Risk":
        recommendation = "Work on improving sleep schedule and take short study breaks."
    else:
        recommendation = "Maintain healthy habits and consistent preparation."

    return {
        "anxiety_level": anxiety_level,
        "confidence": confidence,
        "label": label,
        "suggestion": suggestion,
        "risk_score": risk_score,
        "final_status": final_status,
        "recommendation": recommendation
    }