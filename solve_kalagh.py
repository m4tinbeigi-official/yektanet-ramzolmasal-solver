import requests
import http.cookiejar

def solve_kalagh(cookie_file):
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_file)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

    def fnv1a(s: bytes) -> int:
        h = 2166136261
        for b in s:
            h = ((h ^ b) * 16777619) % 4294967296
        return h

    print("fnv1a yektanet:", fnv1a(b"yektanet"))
    
    r = session.get("https://256.yektanet.tech/ramzolmasal/api/kalagh")
    print("First kalagh response:", r.text)
    current = r.json()

    while True:
        if "flag" in current or "YEK{" in str(current):
            print("FOUND FLAG IN KALAGH:", current)
            return current
        shomare = current.get("shomare")
        payam = current.get("payam")
        if shomare is None or payam is None:
            print("Done/Result:", current)
            return current

        prefix = (payam + ":").encode('ascii')
        nonce = 0
        while True:
            target = prefix + str(nonce).encode('ascii')
            h = fnv1a(target)
            if h < 2048:
                break
            nonce += 1

        print(f"Submitting Kalagh #{shomare} with nonce {nonce} (hash={h})")
        resp = session.post("https://256.yektanet.tech/ramzolmasal/api/kalagh", json={"shomare": shomare, "nonce": str(nonce)})
        current = resp.json()
        print("Response:", current)

if __name__ == "__main__":
    solve_kalagh("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
