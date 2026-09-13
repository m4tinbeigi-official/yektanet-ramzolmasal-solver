import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "ya-x"})

sound_candidates = [
    # Proverb: Yek dast seda nadarad / Sounds
    "یک دست صدا ندارد",
    "یک_دست_صدا_ندارد",
    "یک دست بی صداست",
    "یک_دست_بی_صداست",
    "دست",
    "کف",
    "دست زدن",
    "دست_زدن",
    "کف زدن",
    "کف_زدن",
    "سوت",
    "soot",
    "whistle",
    "دهل",
    "dohol",
    "طبل",
    "tabl",
    "ساز",
    "شیپور",
    "زنگ",
    "بوق",
    "آواز دهل",
    "آواز_دهل",
    "آواز دهل از دور خوش است",
    "آواز_دهل_از_دور_خوش_است",
    "avaze_dohol",
    "yek_dast_seda_nadarad",
    "yekdastsedanadarad",
    # Extracted hex from text: 1d424d339a0922
    "1d424d339a0922",
    "1d424d339a0922w8",
]

print(f"Testing {len(sound_candidates)} sound candidates for Ya-X...")

for i, cand in enumerate(sound_candidates):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(sound_candidates)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND YA-X FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
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
