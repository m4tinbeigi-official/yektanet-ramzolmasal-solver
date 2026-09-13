import sys
import http.cookiejar
import requests
import json

cookie_file = sys.argv[1] if len(sys.argv) > 1 else "/Users/ricksabchez/workspace/ramzolmasal_cookies_ebrahimi.txt"

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar(cookie_file)
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

# The crows challenge solver (fnv-1a / token chain)
# Let's inspect / challenge details
chal = session.get("https://256.yektanet.tech/ramzolmasal/api/challenges/kalagh", headers=headers).json()
print("Kalagh challenge:", chal)

# Get crow 0 token and chain
import hashlib

def fnv1a_32(data: bytes) -> int:
    h = 0x811c9dc5
    for b in data:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h

token = chal.get("token") or ""
current_id = 0

for i in range(1, 41):
    # solve nonce for current crow
    found = False
    for nonce in range(10000000):
        test_str = f"{token}:{nonce}".encode()
        h = fnv1a_32(test_str)
        if (h & 0xFFF) == 0: # 3 hex zeros / 12 bits
            # Submit to get next crow
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/kalagh/hop", json={"nonce": nonce, "token": token}, headers=headers).json()
            if r.get("flag"):
                print(f"[!] Got Kalagh Flag: {r.get('flag')}")
                # Submit flag
                sub = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"challenge_id": "kalagh", "flag": r.get('flag')}, headers=headers).json()
                print(" Kalagh submit:", sub)
                found = True
                break
            elif r.get("next_token"):
                token = r.get("next_token")
                print(f" Crow {i} -> next")
                found = True
                break
            else:
                print("Hop response:", r)
                break
    if not found:
        print("Failed on crow", i)
        break
EOF