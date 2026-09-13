import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})

targeted_candidates = [
    # Action verbs of the proverb
    "نمکش می زنند",
    "نمکش_می_زنند",
    "نمکش میزنند",
    "نمکش_میزنند",
    "نمکش بزن",
    "نمکش_بزن",
    "نمک بزن",
    "نمک_بزن",
    "نمک بزنید",
    "نمک_بزنید",
    "نمک بپاش",
    "نمک_بپاش",
    "نمک بپاشید",
    "نمک_بپاشید",
    "نمک سود",
    "نمک_سود",
    "نمکسود",
    "نمک سود کردن",
    "نمک_سود_کردن",
    "شور کن",
    "شور_کن",
    "شور کردن",
    "شور_کردن",
    # Proverb parts
    "هر چه بگندد نمکش می زنند",
    "هر_چه_بگندد_نمکش_می_زنند",
    "هرچه بگندد نمکش می زنند",
    "هرچه_بگندد_نمکش_می_زنند",
    "هر چه بگندد نمکش میزنند",
    "هر_چه_بگندد_نمکش_میزنند",
    "هرچه بگندد نمکش میزنند",
    "هرچه_بگندد_نمکش_میزنند",
    "وای به روزی که بگندد نمک",
    "وای_به_روزی_که_بگندد_نمک",
    "وای به روزی که بگندد نمک!",
    # Finglish verbs
    "namakash_mizanand",
    "namak_bezan",
    "namaksud",
    "namak_sood",
]

print(f"Testing {len(targeted_candidates)} targeted candidates for Khiar...")

for i, cand in enumerate(targeted_candidates):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(targeted_candidates)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND KHIAR FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
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
