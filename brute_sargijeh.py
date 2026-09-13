import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies_rick.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "sargijeh"})

candidates = [
    # Hafez poem
    "زنهار از این بیابان وین راه بی نهایت",
    "زنهار_از_این_بیابان_وین_راه_بی_نهایت",
    "زنهار از این بیابان",
    "زنهار_از_این_بیابان",
    "وین راه بی نهایت",
    "وین_راه_بی_نهایت",
    "راه بی نهایت",
    "راه_بی_نهایت",
    "بیابان",
    "وحشت",
    "کوکب هدایت",
    "کوکب_هدایت",
    "سرگیجه",
    # Rotation / clock
    "یه ربع",
    "یک ربع",
    "یه_ربع",
    "یک_ربع",
    "چرخیدیم",
    "دور خود چرخیدن",
    "دور_خود_چرخیدن",
    # Finglish
    "zenhar_az_in_biaban",
    "rah_bi_nahayat",
    "biaban",
    "kawkab_hedayat",
    "sargijeh",
]

print(f"Testing {len(candidates)} candidates for Sargijeh...")

for i, cand in enumerate(candidates):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(candidates)}] Testing: {flag}")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 SUCCESS SARGIJEH: {flag} -> {res} 🎉🎉🎉\n\n")
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
