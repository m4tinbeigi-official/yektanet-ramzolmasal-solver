import hashlib
import requests
import http.cookiejar
import time

ACCOUNTS = [
    ("یگانه (Yeganeh)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_yeganeh.txt", "09384486139", "2751ee19"),
    ("ابراهیمی (Ebrahimi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_ebrahimi.txt", "09197955215", "2ecd7405"),
]

for name, cookie_p, phone, uid in ACCOUNTS:
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_p)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj
    
    salted_str = f"{phone}{uid}"
    h = hashlib.sha256(salted_str.encode()).hexdigest()
    flag = f"YEK{{{h}}}"
    
    print(f"\n==========================================")
    print(f"Solving Khiar for {name}")
    print(f"Phone: {phone} | ID: {uid} | String: '{salted_str}'")
    print(f"Submitting Flag: {flag}")
    print(f"==========================================")
    
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})
    time.sleep(1)
    
    while True:
        r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}).json()
        if "زیادی تند" in r.get("error", ""):
            time.sleep(6)
            continue
        print(f"🎉 Result for {name}: {r}")
        break
    time.sleep(10.5)
