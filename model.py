from transformers import pipeline

classifier = pipeline(
    "text-classification",
    model="distilbert-base-uncased-finetuned-sst-2-english"
)

def predict_anxiety(text):
    result = classifier(text)[0]

    label = result["label"]
    score = result["score"]
    confidence = round(score, 3)

    if label == "NEGATIVE":
        if score > 0.85:
            anxiety_level = "High"
            suggestion = "Take deep breaths and revise one topic at a time."
        else:
            anxiety_level = "Moderate"
            suggestion = "You seem slightly stressed. Try structured revision planning."
    else:
        anxiety_level = "Low"
        suggestion = "You seem calm. Maintain your preparation rhythm."

    return {
        "label": label,
        "confidence": confidence,
        "anxiety_level": anxiety_level,
        "suggestion": suggestion
    }