print("DEBUG: api.py LOADED")

import sys
import os

# 👇 FORCE PYTHON TO SEE PROJECT ROOT
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, request, jsonify
import joblib
import numpy as np
from .features import extract_features
from scipy.sparse import hstack

MODEL_PATH = os.path.join(PROJECT_ROOT, "models", "phish_detector.joblib")

app = Flask("phishing_api")  # avoid name conflict

@app.route("/")
def home():
    return "<h2>Phishing Detector API Running Successfully</h2>"

@app.route("/ping")
def ping():
    return jsonify({"status": "API alive"}), 200

@app.route("/predict", methods=["POST"])
def predict():
    data = request.json
    url = data.get("url")

    if not url:
        return jsonify({"error": "URL not provided"}), 400

    saved = joblib.load(MODEL_PATH)
    tfidf = saved["tfidf"]
    model = saved["model"]
    num_keys = saved["num_keys"]

    X_text = tfidf.transform([url])

    feats = extract_features(url)
    X_num = np.array([[feats[k] for k in num_keys]])

    X = hstack([X_text, X_num])

    pred = model.predict(X)[0]

    return jsonify({
        "url": url,
        "prediction": "Phishing" if pred == 1 else "Safe"
    })

if __name__ == "__main__":
    print("DEBUG: Starting Flask server...")
    app.run(host="127.0.0.1", port=5000, debug=True)
