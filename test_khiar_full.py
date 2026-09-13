import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})

khiar_full_proverbs = [
    # Full proverb with spaces / underscores / zwnj
    "هر چه بگندد نمکش می‌زنند، وای به روزی که بگندد نمک",
    "هر چه بگندد نمکش می‌زنند وای به روزی که بگندد نمک",
    "هر_چه_بگندد_نمکش_می‌زنند_وای_به_روزی_که_بگندد_نمک",
    "هر چه بگندد نمکش می زنند، وای به روزی که بگندد نمک",
    "هر چه بگندد نمکش می زنند وای به روزی که بگندد نمک",
    "هر_چه_بگندد_نمکش_می_زنند_وای_به_روزی_که_بگندد_نمک",
    "هرچه بگندد نمکش می زنند وای به روزی که بگندد نمک",
    "هرچه_بگندد_نمکش_می_زنند_وای_به_روزی_که_بگندد_نمک",
    "هر چه بگندد نمکش میزنند وای به روزی که بگندد نمک",
    "هر_چه_بگندد_نمکش_میزنند_وای_به_روزی_که_بگندد_نمک",
    "هرچه بگندد نمکش میزنند وای به روزی که بگندد نمک",
    "هرچه_بگندد_نمکش_میزنند_وای_به_روزی_که_بگندد_نمک",
    # Half proverb
    "هر چه بگندد نمکش می‌زنند",
    "هرچه بگندد نمکش می‌زنند",
    "هر_چه_بگندد_نمکش_می‌زنند",
    "هرچه_بگندد_نمکش_می‌زنند",
    "وای به روزی که بگندد نمک",
    "وای_به_روزی_که_بگندد_نمک",
]

print(f"Testing {len(khiar_full_proverbs)} full proverb forms for Khiar...")

for i, cand in enumerate(khiar_full_proverbs):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(khiar_full_proverbs)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND KHIAR FULL PROVERB FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
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
