print("DEBUG: FILE IS RUNNING!")
import sys
import os
import joblib
from .features import extract_features
import numpy as np

# Add root folder to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

MODEL_PATH = "models/phish_detector.joblib"

def predict_url(url):
    saved = joblib.load(MODEL_PATH)
    tfidf = saved["tfidf"]
    model = saved["model"]
    num_keys = saved["num_keys"]

    X_text = tfidf.transform([url])

    feats = extract_features(url)
    X_num = np.array([[feats[k] for k in num_keys]])

    from scipy.sparse import hstack
    X = hstack([X_text, X_num])

    pred = model.predict(X)[0]
    return "Phishing" if pred == 1 else "Safe"

if __name__ == "__main__":
    print("Enter a URL to test:")
    url = input("> ")
    print("\nPrediction:", predict_url(url))
