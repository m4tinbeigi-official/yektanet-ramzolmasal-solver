import requests
import http.cookiejar
import time

ACCOUNTS = [
    ("متین بیگی (m4tinbeigi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies.txt"),
    ("ریک سانچز (Rick Sanchez)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_rick.txt"),
    ("یگانه بیگی (Yeganeh)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_yeganeh.txt"),
    ("تیم ابراهیمی (Ebrahimi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_ebrahimi.txt"),
]

KIMIAGAR_FLAG = "YEK{25bpjruy5dyv67rj5ibyp0c15yds9is66gh2m7zh7spcksjzbupn4b3kczsyayezejq7yxrbh076podnj5gw2lo3kyt1rbwmpdo6exmhsdon1s0vsutq2yd0w32gyttm}"

for name, cookie_p in ACCOUNTS:
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_p)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj
    
    print(f"\n=======================================================")
    print(f"⚗️ Submitting Kimiagar Flag for: {name}")
    print(f"=======================================================")
    
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "kimiagar"})
    time.sleep(1)
    
    while True:
        r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": KIMIAGAR_FLAG}).json()
        if "زیادی تند" in r.get("error", ""):
            time.sleep(6)
            continue
        print(f"  🎉 Kimiagar Result for {name}: {r}")
        break
        
    time.sleep(10.5)

print("\n\nAll accounts submitted for Kimiagar!")
