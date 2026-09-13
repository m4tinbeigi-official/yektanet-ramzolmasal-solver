import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies_rick.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})

khiar_proverbs = [
    # Persian proverbs
    "بزک نمیر بهار میاد کمبزه با خیار میاد",
    "بزک_نمیر_بهار_میاد_کمبزه_با_خیار_میاد",
    "بزک نمیر بهار میاد",
    "بزک_نمیر_بهار_میاد",
    "کمبزه با خیار میاد",
    "کمبزه_با_خیار_میاد",
    "کمبزه با خیار",
    "کمبزه_با_خیار",
    "آبدوغ خیار",
    "آبدوغ_خیار",
    "ابدوغ خیار",
    "ابدوغ_خیار",
    "خیار چنبر",
    "خیار_چنبر",
    "خیار تلخ",
    "خیار_تلخ",
    "خیارشور",
    "خیار_شور",
    "خیار شور",
    "نمک",
    "شور",
    "بانمک",
    # Finglish
    "bozak_namir_bahar_miad",
    "kambeze_ba_khiar_miad",
    "kambeze",
    "kamboze",
    "abdoogh_khiar",
    "khiar_chambar",
    "khiarshoor",
    "khiarshur",
    "namak",
]

print(f"Testing {len(khiar_proverbs)} proverb candidates on Rick account for Khiar...")

for i, cand in enumerate(khiar_proverbs):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(khiar_proverbs)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND KHIAR PROVERB FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
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
