import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "ya-x"})

sound_names = [
    "ساز",
    "آواز",
    "ندا",
    "بانگ",
    "طنین",
    "فریاد",
    "ناقوس",
    "نی",
    "تار",
    "سه تار",
    "سه_تار",
    "دف",
    "سنتور",
    "کرنا",
    "سرنا",
    "شیپور",
    "چنگ",
    "بربط",
    "عود",
    "تنبک",
    "تمبک",
    "نقاره",
    "هورا",
    "سکوت",
    "هیچ",
    "هیچی",
]

print(f"Testing {len(sound_names)} sound instrument names for Ya-X...")

for i, cand in enumerate(sound_names):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(sound_names)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND YA-X SOUND NAME FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
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
