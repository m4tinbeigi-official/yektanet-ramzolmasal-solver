import hashlib
import requests
import http.cookiejar
import time

ACCOUNTS = [
    ("متین بیگی (m4tinbeigi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies.txt", "09127047813", "88004c9a"),
    ("ریک سانچز (Rick Sanchez)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_rick.txt", "09981998202", "88c78d39"),
    ("یگانه (Yeganeh)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_yeganeh.txt", "09384542171", "2751ee19"),
    ("ابراهیمی (Ebrahimi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_ebrahimi.txt", "09194542171", "2ecd7405"),
]

for name, cookie_p, phone, uid in ACCOUNTS:
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_p)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj
    
    print(f"\n==========================================")
    print(f"Solving Khiar for {name} | Phone: {phone} | ID: {uid}")
    print(f"==========================================")
    
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})
    time.sleep(1)
    
    # Generate variations of SHA256(phone + id)
    cands = [
        (hashlib.sha256(f"{phone}{uid}".encode()).hexdigest(), f"{phone}{uid}"),
        (hashlib.sha256(f"{uid}{phone}".encode()).hexdigest(), f"{uid}{phone}"),
        (hashlib.sha256(f"{phone}:{uid}".encode()).hexdigest(), f"{phone}:{uid}"),
        (hashlib.sha256(f"{uid}:{phone}".encode()).hexdigest(), f"{uid}:{phone}"),
        (hashlib.sha256(f"{phone}_{uid}".encode()).hexdigest(), f"{phone}_{uid}"),
        (hashlib.sha256(f"{uid}_{phone}".encode()).hexdigest(), f"{uid}_{phone}"),
        (hashlib.sha256(f"{phone} {uid}".encode()).hexdigest(), f"{phone} {uid}"),
        (hashlib.sha256(f"{uid} {phone}".encode()).hexdigest(), f"{uid} {phone}"),
        (hashlib.sha256(f"{phone.lstrip('0')}{uid}".encode()).hexdigest(), f"{phone.lstrip('0')}{uid}"),
        (hashlib.sha256(f"{uid}{phone.lstrip('0')}".encode()).hexdigest(), f"{uid}{phone.lstrip('0')}"),
        (hashlib.md5(f"{phone}{uid}".encode()).hexdigest(), f"md5({phone}{uid})"),
    ]
    
    for h, desc in cands:
        flag = f"YEK{{{h}}}"
        print(f"Submitting: {flag[:35]}... ({desc})")
        while True:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}).json()
            if "زیادی تند" in r.get("error", ""):
                time.sleep(6)
                continue
            if r.get("correct"):
                print(f"\n🎉🎉🎉 SUCCESS FOR KHIAR ({name}): {flag} -> {r} 🎉🎉🎉\n")
                break
            else:
                pass
            break
        if r.get("correct"):
            break
        time.sleep(10.5)
