import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})

namak_proverbs = [
    # Hand without salt
    "دست بی نمک",
    "دست_بی_نمک",
    "دستم نمک نداره",
    "دستم_نمک_نداره",
    "دستش نمک نداره",
    "دستش_نمک_نداره",
    "نمک نشناس",
    "نمک_نشناس",
    "نان و نمک",
    "نان_و_نمک",
    "نون و نمک",
    "نون_و_نمک",
    "نمک گیر",
    "نمک_گیر",
    "نمک پرورده",
    "نمک_پرورده",
    "نمک به حرام",
    "نمک_به_حرام",
    "نمک به زخم",
    "نمک_به_زخم",
    "نمک رو زخم",
    "نمک_رو_زخم",
    "نمکدان شکستن",
    "نمکدان_شکستن",
    "نمک خوردن و نمکدان شکستن",
    "نمک_خوردن_و_نمکدان_شکستن",
    # Abjad 110 + Phone
    "09127047923",
    "9127047923",
    "110",
    # Finglish
    "dast_bi_namak",
    "dastam_namak_nadareh",
    "namak_nashnas",
    "noon_o_namak",
    "namakgir",
    "namakparvardeh",
    "namak_roozakhm",
]

print(f"Testing {len(namak_proverbs)} Namak proverbs for Khiar...")

for i, cand in enumerate(namak_proverbs):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(namak_proverbs)}] Submitting: {flag}...")
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
