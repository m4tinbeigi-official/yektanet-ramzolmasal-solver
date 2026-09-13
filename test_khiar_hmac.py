import hmac
import hashlib
import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})

phones = ["09127047813", "9127047813", "+989127047813", "0912***7813"]
keys = ["namak", "نمک", "salt", "banamak", "بانمک", "khiar", "خیار", "88004c9a", "m4tinbeigi"]

hmac_candidates = []

for p in phones:
    for k in keys:
        # HMAC-SHA256
        h1 = hmac.new(k.encode('utf-8'), p.encode('utf-8'), hashlib.sha256).hexdigest()
        h2 = hmac.new(p.encode('utf-8'), k.encode('utf-8'), hashlib.sha256).hexdigest()
        hmac_candidates.extend([h1, h2])

print(f"Generated {len(hmac_candidates)} HMAC candidates for Khiar.")

for i, cand in enumerate(hmac_candidates):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(hmac_candidates)}] Submitting: {flag[:30]}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND KHIAR HMAC FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
                with open("/Users/ricksabchez/workspace/khiar_flag.txt", "w") as f:
                    f.write(flag)
                exit(0)
            else:
                print(f"  -> Wrong: {res.get('message')}")
                break
        except Exception as e:
            print("Error:", e)
            time.sleep(5)
    time.sleep(10.5)
