import hashlib
import base64
import requests
import http.cookiejar

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

my_id = "88004c9a"
print("My ID:", my_id)

candidates = [
    my_id,
    hashlib.sha256(my_id.encode()).hexdigest(),
    base64.b64encode(my_id.encode()).decode(),
    base64.b64encode(hashlib.sha256(my_id.encode()).digest()).decode(),
    "rubah",
    "shahed",
    "shahed-rubah",
    "shahed_rubah",
    "دم روباه",
    "دمش",
    "دم",
    "دم_روباه",
    "شاهد روباه دمش است",
    "شاهد_روباه_دمش_است",
    "شاهد روباه دمش",
    "شاهد روباه، دمش",
    "YEK{" + my_id + "}",
    "YEK{" + hashlib.sha256(my_id.encode()).hexdigest() + "}",
    "YEK{" + base64.b64encode(my_id.encode()).decode() + "}",
    "YEK{shahed}",
    "YEK{rubah}",
    "YEK{shahed_rubah}",
    "YEK{دمش}",
    "YEK{دم روباه}",
    "YEK{دم_روباه}",
    "YEK{دمش است}",
    "YEK{دمش_است}",
    "YEK{شاهد_روباه}",
]

for cand in candidates:
    flag = cand if cand.startswith("YEK{") else f"YEK{{{cand}}}"
    r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag})
    res = r.json()
    if res.get("correct"):
        print(f"!!! SUCCESS FOR SHAHED: {flag} -> {res}")
        break
    else:
        # print first few fails
        pass
else:
    print("Direct candidates did not match, investigating deeper...")
