import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "sargijeh"})

with open('/Users/ricksabchez/workspace/rot_candidates.txt', 'r') as f:
    candidates = [line.strip() for line in f if line.strip()]

print(f"Testing {len(candidates)} ROT candidates for Sargijeh...")

for i, cand in enumerate(candidates):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(candidates)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND SARGIJEH ROT FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
                with open("/Users/ricksabchez/workspace/sargijeh_flag.txt", "w") as f:
                    f.write(flag)
                exit(0)
            else:
                print(f"  -> Wrong: {res.get('message')}")
                break
        except Exception as e:
            print("Error:", e)
            time.sleep(5)
    time.sleep(10.5)
