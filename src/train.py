# src/train.py

import os
import numpy as np
import pandas as pd
from joblib import dump
from scipy.sparse import hstack

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

# IMPORTANT: this import only works if src/__init__.py exists
from src.features import extract_features


# -------------------------------
# Load CSV Dataset
# -------------------------------
def load_data(path="data/sample_urls.csv"):
    df = pd.read_csv(path)
    df = df.dropna(subset=["url"])
    return df


# -------------------------------
# Convert URL → Numeric Features
# -------------------------------
def lexical_feature_matrix(urls):
    feature_dicts = [extract_features(u) for u in urls]

    keys = [
        "url_length",
        "digits",
        "special",
        "https",
        "subdomains",
        "suspicious_token",
        "host_entropy"
    ]

    X = np.array([[fd[k] for k in keys] for fd in feature_dicts], dtype=float)
    return X, keys


# -------------------------------
# Create TF-IDF Vectorizer
# -------------------------------
def make_vectorizer():
    return TfidfVectorizer(
        analyzer="char_wb",
        ngram_range=(3, 5)
    )


# -------------------------------
# TRAIN MODEL
# -------------------------------
def train(
    path="data/sample_urls.csv",
    model_out="models/phish_detector.joblib"
):
    df = load_data(path)

    urls = df["url"].astype(str).tolist()
    y = df["label"].astype(int).values

    # Text vectorizer
    tfidf = make_vectorizer()
    X_text = tfidf.fit_transform(urls)

    # Numeric lexical features
    X_num, num_keys = lexical_feature_matrix(urls)

    # Merge sparse + dense
    X = hstack([X_text, X_num])

    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y,
        test_size=0.2,
        random_state=42,
        stratify=y if len(set(y)) > 1 else None
    )

    # Classifier
    clf = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )
    clf.fit(X_train, y_train)

    # Evaluate
    y_pred = clf.predict(X_test)
    print("\n===== CLASSIFICATION REPORT =====")
    print(classification_report(y_test, y_pred, zero_division=0))

    # Save model + vectorizer
    os.makedirs(os.path.dirname(model_out), exist_ok=True)
    dump(
        {"tfidf": tfidf, "model": clf, "num_keys": num_keys},
        model_out
    )

    print("\nModel saved to:", model_out)


# Entry point
if __name__ == "__main__":
    train()
