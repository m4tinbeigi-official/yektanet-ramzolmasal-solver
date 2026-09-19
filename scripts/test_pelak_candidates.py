import hashlib
import requests
import http.cookiejar
import time

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "pelak"})
time.sleep(1)

mobile = "09127047813"
phones = [
    # Yektanet known landline phone numbers or prefixes
    "02191070256", "02191000256", "02125600000", "021256", "0256", "256",
    "037", "037256", "0370000", "02188888888", "02191070000", "0219107",
    "0219100", "021910", "91070256", "91000256", "021",
]

cands = []
for p in phones:
    cands.append(f"{p}{mobile}")
    cands.append(f"{mobile}{p}")
    cands.append(f"{p}:{mobile}")
    cands.append(f"{mobile}:{p}")
    cands.append(f"{p}_{mobile}")
    cands.append(f"{mobile}_{p}")
    # Also hashes of these
    cands.append(hashlib.sha256(f"{p}{mobile}".encode()).hexdigest())
    cands.append(hashlib.sha256(f"{mobile}{p}".encode()).hexdigest())
    cands.append(hashlib.md5(f"{p}{mobile}".encode()).hexdigest())

print(f"Testing {len(cands)} candidates for Pelak (دیوار به دیوار)...")

for i, cand in enumerate(cands):
    flag = f"YEK{{{cand}}}"
    print(f"[{i+1}/{len(cands)}] Submitting: {flag[:40]}...")
    while True:
        r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}).json()
        if "زیادی تند" in r.get("error", ""):
            time.sleep(6)
            continue
        if r.get("correct"):
            print(f"\n🎉🎉🎉 SUCCESS FOR PELAK: {flag} -> {r} 🎉🎉🎉\n")
            with open("/Users/ricksabchez/workspace/pelak_flag.txt", "w") as f:
                f.write(flag)
            exit(0)
        else:
            print(f"  Result: {r.get('message')}")
        break
    time.sleep(10.5)
