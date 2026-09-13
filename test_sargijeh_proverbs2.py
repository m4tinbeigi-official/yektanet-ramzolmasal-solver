import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

# Test for sargijeh
session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "sargijeh"})

mill_candidates = [
    # Asiyab / Mill proverbs
    "آسیاب به نوبت",
    "آسیاب_به_نوبت",
    "آسیاب",
    "اسیاب",
    "چرخ و فلک",
    "چرخ_و_فلک",
    "چرخ",
    "فلک",
    "خرخر",
    "تق تق",
    "تق_تق",
    "صدای خرخر",
    "صدای_خرخر",
    "شنگول و منگول",
    "شنگول_و_منگول",
    "حبه انگور",
    "حبه_انگور",
    "گرگ ناقلا",
    "گرگ_ناقلا",
    "بزک زنگوله پا",
    "بزک_زنگوله_پا",
    "asiyab_be_nobat",
    "asiyab",
    "charkh_o_falak",
    "charkh",
]

print(f"Testing {len(mill_candidates)} proverb candidates for Sargijeh...")

for i, cand in enumerate(mill_candidates):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(mill_candidates)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND SARGIJEH FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
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
