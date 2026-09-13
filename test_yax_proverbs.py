import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "ya-x"})

yax_proverbs = [
    # Yek dast seda nadarad variants
    "یک دست صدا نداره",
    "یک_دست_صدا_نداره",
    "یکدست صدا ندارد",
    "یکدست_صدا_ندارد",
    "یکدست صدا نداره",
    "یکدست_صدا_نداره",
    "یک دست بی صداست",
    "یک_دست_بی_صداست",
    "یک دست بی صدا است",
    "یک_دست_بی_صدا_است",
    "دست تنها صدا نداره",
    "دست_تنها_صدا_نداره",
    "دست تنها صدا ندارد",
    "دست_تنها_صدا_ندارد",
    "صدای یک دست",
    "صدای_یک_دست",
    "دست زدن",
    "دست_زدن",
    "کف زدن",
    "کف_زدن",
    "کف",
    "دست",
    "هورا",
    "تشویق",
    "دست_تنها",
    "دست تنها",
    "صدا ندارد",
    "صدا_ندارد",
    "صدا نداره",
    "صدا_نداره",
    "بی صدا",
    "بی_صدا",
    # Finglish
    "yek_dast_seda_nadareh",
    "yek_dast_seda_nadarad",
    "yekdastsedanadareh",
    "dast_tanha_seda_nadarad",
]

print(f"Testing {len(yax_proverbs)} proverb candidates for Ya-X...")

for i, cand in enumerate(yax_proverbs):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(yax_proverbs)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND YA-X PROVERB FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
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
