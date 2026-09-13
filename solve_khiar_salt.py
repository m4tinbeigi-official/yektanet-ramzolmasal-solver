import hashlib
import base64
import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})

phone = "09127047813"
my_id = "88004c9a"
nickname = "m4tinbeigi"

# Generate hashes
hashes = []

# 1. phone with id as salt
for sep in ["", ":", "-", "_", "/", "|"]:
    s1 = f"{phone}{sep}{my_id}"
    s2 = f"{my_id}{sep}{phone}"
    hashes.append(hashlib.sha256(s1.encode()).hexdigest())
    hashes.append(hashlib.sha256(s2.encode()).hexdigest())
    hashes.append(hashlib.md5(s1.encode()).hexdigest())
    hashes.append(hashlib.md5(s2.encode()).hexdigest())

# 2. phone with nickname as salt
for sep in ["", ":"]:
    s1 = f"{phone}{sep}{nickname}"
    s2 = f"{nickname}{sep}{phone}"
    hashes.append(hashlib.sha256(s1.encode()).hexdigest())
    hashes.append(hashlib.sha256(s2.encode()).hexdigest())

# 3. Base64
hashes.append(base64.b64encode(f"{phone}:{my_id}".encode()).decode())
hashes.append(base64.b64encode(f"{phone}{my_id}".encode()).decode())

# 4. XOR phone and id
min_len = min(len(phone), len(my_id))
x1 = bytes([phone.encode()[i] ^ my_id.encode()[i] for i in range(min_len)])
hashes.append(x1.hex())
hashes.append(base64.b64encode(x1).decode())
hashes.append(hashlib.sha256(x1).hexdigest())

# 5. Salt word combinations
for salt_word in ["namak", "نمک", "salt", "banamak", "بانمک"]:
    for p in [phone, "9127047813", "+989127047813", "0912***7813"]:
        hashes.append(hashlib.sha256(f"{p}:{salt_word}".encode()).hexdigest())
        hashes.append(hashlib.sha256(f"{p}{salt_word}".encode()).hexdigest())
        hashes.append(hashlib.sha256(f"{salt_word}:{p}".encode()).hexdigest())
        hashes.append(hashlib.sha256(f"{salt_word}{p}".encode()).hexdigest())
        hashes.append(hashlib.md5(f"{p}:{salt_word}".encode()).hexdigest())
        hashes.append(hashlib.md5(f"{p}{salt_word}".encode()).hexdigest())

print(f"Total {len(hashes)} candidate flags for Khiar.")

for i, h in enumerate(hashes):
    flag = f"YEK{{{h}}}"
    print(f"[{i+1}/{len(hashes)}] Testing: {flag[:30]}...")
    while True:
        try:
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}, timeout=10)
            res = r.json()
            if "زیادی تند" in res.get("error", ""):
                time.sleep(6)
                continue
            if res.get("correct"):
                print(f"\n\n🎉🎉🎉 SUCCESS FOR KHIAR: {flag} -> {res} 🎉🎉🎉\n\n")
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
