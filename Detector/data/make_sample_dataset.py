# data/make_sample_dataset.py
import pandas as pd

phish = [
    "http://login-secure.example.com/verify",
    "http://secure-paypal.example.org/login",
    "http://update-account.example.net/index.php",
    "http://xn--bank-login-123.com/confirm",
    "http://free-gift.example.com/claim"
]

legit = [
    "https://www.google.com/search?q=python",
    "https://github.com/user/repo",
    "https://en.wikipedia.org/wiki/Phishing",
    "https://stackoverflow.com/questions/12345/example",
    "https://example.com/about"
]

df_phish = pd.DataFrame({"url": phish, "label": 1})
df_legit = pd.DataFrame({"url": legit, "label": 0})

df = pd.concat([df_phish, df_legit], ignore_index=True)
df.to_csv("data/sample_urls.csv", index=False)
print("Wrote data/sample_urls.csv with", len(df), "rows")
