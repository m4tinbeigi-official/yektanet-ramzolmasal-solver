import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "ya-x"})

donkey_sounds = [
    "عرعر",
    "عر عر",
    "عر_عر",
    "عر",
    "صدای خر",
    "صدای_خر",
    "صدای الاغ",
    "صدای_الاغ",
    "عرعر خر",
    "عرعر_خر",
    "arar",
    "ar_ar",
    "ar-ar",
    "khar",
    "olagh",
    "donkey",
    "bray",
    "hee-haw",
    "heehaw",
]

print(f"Testing {len(donkey_sounds)} donkey sound candidates for Ya-X...")

for i, cand in enumerate(donkey_sounds):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(donkey_sounds)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND YA-X DONKEY FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
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
