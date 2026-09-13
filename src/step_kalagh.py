import subprocess
import requests
import http.cookiejar
import time

def run_kalagh():
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

    r = session.get("https://256.yektanet.tech/ramzolmasal/api/kalagh")
    print("Initial Kalagh:", r.status_code, r.text)
    data = r.json()

    for step in range(1, 100):
        if "flag" in data or "YEK{" in str(data):
            print("FOUND KALAGH FLAG:", data)
            return data
        shomare = data.get("shomare")
        payam = data.get("payam")
        if not shomare or not payam:
            print("Finished / No more steps:", data)
            break
        
        t0 = time.time()
        nonce = subprocess.check_output(["/Users/ricksabchez/workspace/fast_nonce", payam]).decode().strip()
        t1 = time.time()
        resp = session.post("https://256.yektanet.tech/ramzolmasal/api/kalagh", json={"shomare": shomare, "nonce": nonce})
        print(f"Step {shomare} | Nonce: {nonce} | Calc time: {t1-t0:.4f}s | HTTP Status: {resp.status_code} | Body: {resp.text}")
        data = resp.json()

if __name__ == "__main__":
    run_kalagh()
