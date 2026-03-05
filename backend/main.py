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
    try:
        response = requests.post(
            HF_API_URL,
            headers=headers,
            json={"inputs": data.text},
            timeout=30
        )

        result_json = response.json()

        # If HF returns error message
        if "error" in result_json:
            return {"error_from_huggingface": result_json}

        # Handle nested structure safely
        if isinstance(result_json, list):
            if isinstance(result_json[0], list):
                result = result_json[0][0]
            else:
                result = result_json[0]
        else:
            return {"unexpected_response": result_json}

        label = result["label"]
        score = result["score"]

        anxiety_level = (
            "High" if label == "NEGATIVE" and score > 0.85
            else "Moderate" if label == "NEGATIVE"
            else "Low"
        )

        return {
            "label": label,
            "confidence": round(score, 3),
            "anxiety_level": anxiety_level
        }

    except Exception as e:
        return {"server_error": str(e)}