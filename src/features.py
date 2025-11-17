# src/features.py
import re
import math
from urllib.parse import urlparse
import tldextract
import numpy as np

def url_length(url):
    return len(url)

def count_digits(url):
    return sum(c.isdigit() for c in url)

def count_special(url):
    return sum(1 for c in url if c in "/-@?_=&%$")

def has_https(url):
    return 1 if url.lower().startswith("https") else 0

def count_subdomains(url):
    ext = tldextract.extract(url)
    sub = ext.subdomain
    if not sub:
        return 0
    return sub.count('.') + 1

def suspicious_token_present(url, tokens=None):
    if tokens is None:
        tokens = ["login","secure","account","update","verify","bank","confirm","webscr","signin","pay","admin"]
    lower = url.lower()
    return int(any(tok in lower for tok in tokens))

def hostname_entropy(url):
    try:
        ext = tldextract.extract(url)
        host = ext.subdomain + ext.domain
        if not host:
            host = url
        probs = [host.count(c)/len(host) for c in set(host)]
        ent = -sum(p*math.log(p+1e-12,2) for p in probs)
        return ent
    except Exception:
        return 0.0

def extract_features(url):
    feats = {
        "url_length": url_length(url),
        "digits": count_digits(url),
        "special": count_special(url),
        "https": has_https(url),
        "subdomains": count_subdomains(url),
        "suspicious_token": suspicious_token_present(url),
        "host_entropy": hostname_entropy(url)
    }
    return feats
