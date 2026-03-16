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
        "rating": "Excellent"     if predicted_score >= 90 else
                  "Very Good"     if predicted_score >= 80 else
                  "Good"          if predicted_score >= 70 else
                  "Average"       if predicted_score >= 60 else
                  "Below Average" if predicted_score >= 50 else
                  "Poor"
    })

# Compare.
@app.route("/compare", methods=["POST"])
def compare():
    data = request.json
    phone_a = data["phone_a"]
    phone_b = data["phone_b"]

    def get_features(phone):
        return pd.DataFrame([{
            "back_camera":   phone["back_camera"],
            "battery":       phone["battery"],
            "display":       phone["display"],
            "ram":           phone["ram"],
            "brand_encoded": phone["brand_encoded"],
            "tier_encoded":  phone["tier_encoded"]
        }])

    # Score both phones.
    score_a = round(float(score_model.predict(get_features(phone_a))[0]), 2)
    score_b = round(float(score_model.predict(get_features(phone_b))[0]), 2)

    # Price prediction both phones.
    pred_a = "increase" if model.predict(get_features(phone_a))[0] == 1 else "decrease"
    pred_b = "increase" if model.predict(get_features(phone_b))[0] == 1 else "decrease"

    def get_rating(score):
        if score >= 90:   return "Excellent"
        elif score >= 80: return "Very Good"
        elif score >= 70: return "Good"
        elif score >= 60: return "Average"
        elif score >= 50: return "Below Average"
        else:             return "Poor"

    # Winner.
    if score_a > score_b:
        winner = phone_a.get("name", "Phone A")
        margin = round(score_a - score_b, 2)
    elif score_b > score_a:
        winner = phone_b.get("name", "Phone B")
        margin = round(score_b - score_a, 2)
    else:
        winner = "Tie"
        margin = 0

    return jsonify({
        "phone_a": {
            "name":       phone_a.get("name", "Phone A"),
            "score":      score_a,
            "rating":     get_rating(score_a),
            "prediction": pred_a
        },
        "phone_b": {
            "name":       phone_b.get("name", "Phone B"),
            "score":      score_b,
            "rating":     get_rating(score_b),
            "prediction": pred_b
        },
        "winner": winner,
        "score_margin": margin
    })

if __name__ == "__main__":
    app.run(debug=True)

