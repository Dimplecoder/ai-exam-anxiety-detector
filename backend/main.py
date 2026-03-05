@app.post("/predict")
def predict(data: TextInput):
    response = requests.post(
        HF_API_URL,
        headers=headers,
        json={"inputs": data.text}
    )

    result_json = response.json()

    # Handle nested response safely
    if isinstance(result_json[0], list):
        result = result_json[0][0]
    else:
        result = result_json[0]

    label = result["label"]
    score = result["score"]

    anxiety_level = "High" if label == "NEGATIVE" and score > 0.85 else \
                    "Moderate" if label == "NEGATIVE" else "Low"

    return {
        "label": label,
        "confidence": round(score, 3),
        "anxiety_level": anxiety_level
    }