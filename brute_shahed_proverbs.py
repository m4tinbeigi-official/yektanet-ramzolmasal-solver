import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "shahed"})

candidates = [
    # Persian
    "دمم",
    "دمش",
    "دم",
    "دم روباه",
    "دم_روباه",
    "دم-روباه",
    "شاهد روباه دمش است",
    "شاهد_روباه_دمش_است",
    "شاهد روباه دمش",
    "شاهد_روباه_دمش",
    "به روباه گفتند شاهدت کیه گفت دمم",
    "به_روباه_گفتند_شاهدت_کیه_گفت_دمم",
    # Finglish
    "domam",
    "domash",
    "dom",
    "dome_roobah",
    "dome-roobah",
    "domeroobah",
    "dome_rubah",
    "domerubah",
    # English
    "tail",
    "my_tail",
    "his_tail",
    "fox_tail",
    "foxtail",
    "fox-tail",
    "witness",
    "self",
    "myself",
]

print(f"Total {len(candidates)} candidates to test.")

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
                print(f"\n\n🎉🎉🎉 SUCCESS: {flag} -> {res} 🎉🎉🎉\n\n")
                with open("/Users/ricksabchez/workspace/shahed_flag.txt", "w") as f:
                    f.write(flag)
                exit(0)
            else:
                print(f"  -> Wrong: {res.get('message')}")
                break
        except Exception as e:
            print("Error:", e)
            time.sleep(5)
    time.sleep(10.5)
