from flask import Flask, jsonify, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model once at startup.
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

with open("score_model.pkl", "rb") as f:
    score_model = pickle.load(f)

# Home.
@app.route("/", methods=["GET"])
def home():
    return jsonify({"message": "Homepage 🐯🏡⭐"})


# Predict.
@app.route("/predict", methods=["POST"])
def predict():
    data = request.json

    features = pd.DataFrame([{
        "back_camera":   data["back_camera"],
        "battery":       data["battery"],
        "display":       data["display"],
        "ram":           data["ram"],
        "brand_encoded": data["brand_encoded"],
        "tier_encoded":  data["tier_encoded"]
    }])

    prediction = model.predict(features)[0]
    result = "increase" if prediction == 1 else "decrease"

    return jsonify({
        "phone":      data.get("name", "Unknown"),
        "prediction": result
    })

# Score.
@app.route("/score", methods=["POST"])
def score():
    data = request.json

    features = pd.DataFrame([{
        "back_camera":   data["back_camera"],
        "battery":       data["battery"],
        "display":       data["display"],
        "ram":           data["ram"],
        "brand_encoded": data["brand_encoded"],
        "tier_encoded":  data["tier_encoded"]
    }])

    predicted_score = score_model.predict(features)[0]

    return jsonify({
        "phone": data.get("name", "Unknown"),
        "score": round(float(predicted_score), 2),
        "rating": "Excellent" if predicted_score >= 80 else
                  "Good"      if predicted_score >= 60 else
                  "Average"   if predicted_score >= 40 else
                  "Budget"
    })

if __name__ == "__main__":
    app.run(debug=True)

    