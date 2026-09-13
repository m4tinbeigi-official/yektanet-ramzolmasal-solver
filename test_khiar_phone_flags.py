import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})

phone_flags = [
    "YEK{8c44e98dc38a15b043db264cd4399409ed89c61b21a2f9f0c79c3babbb89835f}",
    "YEK{jETpjcOKFbBD2yZM1DmUCe2Jxhshovnwx5w7q7uJg18=}",
    "YEK{MDkxMjcwNDc4MTM=}",
    "YEK{1c7ef6c036a5b9bcfdba549a3d15d380ebd66f8cbed9bb6cf9041a2cbfe3bd93}",
    "YEK{HH72wDalubz9ulSaPRXTgOvWb4y+2bts+QQaLL/jvZM=}",
    "YEK{OTEyNzA0NzgxMw==}",
    "YEK{7f53f7b42a7b894365a4d31880604d9df26209c441c18ea7192ddf519e301151}",
    "YEK{f1P3tCp7iUNlpNMYgGBNnfJiCcRBwY6nGS3fUZ4wEVE=}",
    "YEK{Kzk4OTEyNzA0NzgxMw==}",
    "YEK{3137f834ba075d252b0975d22e80e31909a9de097bbeaa47b953ac1ad3b78649}",
    "YEK{MTf4NLoHXSUrCXXSLoDjGQmp3gl7vqpHuVOsGtO3hkk=}",
    "YEK{239d7c786cecfb165be42321146b7a03f21c651d5dae2c6dbaa94fa3fadcd64e}",
    "YEK{I518eGzs+xZb5CMhFGt6A/IcZR1drixtuqlPo/rc1k4=}",
]

print("Testing phone-derived flags for Khiar...")

for i, flag in enumerate(phone_flags):
    print(f"[{i+1}/{len(phone_flags)}] Submitting: {flag}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 FOUND KHIAR PHONE FLAG: {flag} -> {res} 🎉🎉🎉\n\n")
                with open("/Users/ricksabchez/workspace/khiar_flag.txt", "w") as f:
                    f.write(flag)
                exit(0)
            else:
                print(f"  -> Wrong: {res.get('message')}")
                break
        except Exception as e:
            print("Error:", e)
            time.sleep(5)
    time.sleep(10.5)
