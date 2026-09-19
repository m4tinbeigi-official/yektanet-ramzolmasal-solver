import hashlib
import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

def submit_flag(level_id, flag):
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": level_id})
    try:
        r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
        res = r.json()
        if res.get("correct"):
            print(f"\n\n🎉🎉🎉 SUCCESS FOR {level_id}: {flag} -> {res} 🎉🎉🎉\n\n")
            with open(f"/Users/ricksabchez/workspace/{level_id}_solved_flag.txt", "w") as f:
                f.write(flag)
            return True
        else:
            print(f"[{level_id}] {flag[:35]} -> Wrong")
            return False
    except Exception as e:
        print("Error:", e)
        return False

# Focus candidates for ya-x
yax_cands = [
    "YEK{1d424d339a0922w8}",
    "YEK{1d424d339a0922}",
    "YEK{hiss}",
    "YEK{فس}",
    "YEK{فیس}",
    "YEK{هیس}",
    "YEK{فشش}",
    "YEK{سوت}",
    "YEK{خرخر}",
    "YEK{مار}",
    "YEK{AU}",
    "YEK{Au}",
    "YEK{au}",
    "YEK{gold}",
    "YEK{طلا}",
]

for flag in yax_cands:
    if submit_flag("ya-x", flag):
        break
    time.sleep(6)
