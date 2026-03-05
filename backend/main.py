from fastapi import FastAPI
from pydantic import BaseModel
from transformers import pipeline

app = FastAPI()

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

class TextInput(BaseModel):
    text: str

@app.get("/")
def home():
    return {"message": "Backend is working"}

@app.post("/predict")
def predict(data: TextInput):
    result = classifier(data.text)[0]

    label = result["label"]
    score = result["score"]

    if label == "NEGATIVE":
        anxiety_level = "High" if score > 0.85 else "Moderate"
    else:
        anxiety_level = "Low"

    return {
        "label": label,
        "confidence": round(score, 3),
        "anxiety_level": anxiety_level
    }