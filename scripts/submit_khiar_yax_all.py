import hashlib
import requests
import http.cookiejar
import time

ACCOUNTS = [
    ("متین بیگی (m4tinbeigi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies.txt", "09127047813"),
    ("ریک سانچز (Rick Sanchez)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_rick.txt", "09981998202"),
    ("یگانه (Yeganeh)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_yeganeh.txt", "09384542171"),
    ("ابراهیمی (Ebrahimi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_ebrahimi.txt", "09194542171"),
]

YAX_FLAG = "YEK{8b20d2e007c740e35428d1bbdd964654}"

for name, cookie_p, phone in ACCOUNTS:
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_p)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj
    
    me = session.get("https://256.yektanet.tech/ramzolmasal/api/me").json()
    user_id = me.get("id")
    print(f"\n=======================================================")
    print(f"🚀 Submitting Khiar & Ya-X for: {name} (ID: {user_id}, Phone: {phone})")
    print(f"=======================================================")
    
    # 1. Solve Khiar: SHA256(phone + user_id)
    khiar_input = f"{phone}{user_id}"
    khiar_hash = hashlib.sha256(khiar_input.encode()).hexdigest()
    khiar_flag = f"YEK{{{khiar_hash}}}"
    
    print(f"🔹 [1/2] Submitting Khiar flag: {khiar_flag} (from '{khiar_input}')")
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})
    time.sleep(1)
    
    while True:
        r_khiar = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": khiar_flag}).json()
        if "زیادی تند" in r_khiar.get("error", ""):
            time.sleep(6)
            continue
        print(f"  👉 Khiar result: {r_khiar}")
        break
        
    time.sleep(10.5)
    
    # 2. Solve Ya-X
    print(f"🔹 [2/2] Submitting Ya-X flag: {YAX_FLAG}")
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "ya-x"})
    time.sleep(1)
    
    while True:
        r_yax = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": YAX_FLAG}).json()
        if "زیادی تند" in r_yax.get("error", ""):
            time.sleep(6)
            continue
        print(f"  👉 Ya-X result: {r_yax}")
        break
        
    time.sleep(10.5)

print("\n\nAll submissions completed!")
