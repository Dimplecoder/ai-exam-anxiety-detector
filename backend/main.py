from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os

app = FastAPI()

HF_API_URL = "https://api-inference.huggingface.co/models/distilbert-base-uncased-finetuned-sst-2-english"
HF_TOKEN = os.getenv("HF_TOKEN")

headers = {
    "Authorization": f"Bearer {HF_TOKEN}"
}

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Backend is working"}

@app.post("/predict")
def predict(data: TextInput):
    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": data.text}
    )

    result = response.json()[0]

    label = result["label"]
    score = result["score"]

    anxiety_level = "High" if label == "NEGATIVE" and score > 0.85 else \
                    "Moderate" if label == "NEGATIVE" else "Low"

    return {
        "label": label,
        "confidence": round(score, 3),
        "anxiety_level": anxiety_level
    }