import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "ya-x"})

freq_candidates = [
    "256",
    "256Hz",
    "256_hz",
    "256hz",
    "1000",
    "1000Hz",
    "1000hz",
    "1000_hz",
    "440",
    "440Hz",
    "440hz",
    "440_hz",
    "800",
    "1200",
    "512",
    "1024",
    "2048",
    "1367",
    "1368",
]

print(f"Testing {len(freq_candidates)} frequency candidates for Ya-X...")

for i, cand in enumerate(freq_candidates):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(freq_candidates)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND YA-X FREQUENCY FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
                with open("/Users/ricksabchez/workspace/yax_flag.txt", "w") as f:
                    f.write(flag)
                exit(0)
            else:
                print(f"  -> Wrong: {res.get('message')}")
                break
        except Exception as e:
            print("Error:", e)
            time.sleep(5)
    time.sleep(10.5)
