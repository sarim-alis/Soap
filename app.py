from flask import Flask, jsonify, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load model once at startup.
with open("model.pkl", "rb") as f:
    model = pickle.load(f)

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

if __name__ == "__main__":
    app.run(debug=True)

    