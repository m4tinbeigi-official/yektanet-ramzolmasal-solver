import hashlib
import base64
import requests
import http.cookiejar

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

my_id = "88004c9a"
nickname = "m4tinbeigi"
phone = "09127047813"

# Let's emulate ctf helper functions:
# hash(x) -> sha256 hex
# khord(x) -> sha256 bytes
# setabr(x) -> base64(x)
# xor(a, b) -> a ^ b

def ctf_hash(s):
    if isinstance(s, str): s = s.encode('utf-8')
    return hashlib.sha256(s).hexdigest()

def ctf_khord(s):
    if isinstance(s, str): s = s.encode('utf-8')
    return hashlib.sha256(s).digest()

def ctf_setabr(b):
    if isinstance(b, str): b = b.encode('utf-8')
    return base64.b64encode(b).decode('utf-8')

def ctf_xor(b1, b2):
    if isinstance(b1, str): b1 = b1.encode('utf-8')
    if isinstance(b2, str): b2 = b2.encode('utf-8')
    min_len = min(len(b1), len(b2))
    res = bytes([b1[i] ^ b2[i] for i in range(min_len)])
    return res

# Generate candidates
candidates = []

# ID operations
candidates.append(my_id)
candidates.append(ctf_hash(my_id))
candidates.append(ctf_setabr(my_id))
candidates.append(ctf_setabr(ctf_khord(my_id)))
candidates.append(ctf_hash(ctf_setabr(my_id)))

# XOR self:
# xor(my_id, my_id) -> all 0s
candidates.append(ctf_setabr(ctf_xor(my_id, my_id)))

# Combine ID and prompt/title/rubah/shahed
for word in ["shahed", "rubah", "fox", "witness", "m4tinbeigi", "شاهد", "روباه"]:
    candidates.append(ctf_hash(word))
    candidates.append(ctf_setabr(word))
    candidates.append(ctf_setabr(ctf_khord(word)))
    # XOR with my_id
    x = ctf_xor(my_id, word)
    candidates.append(ctf_setabr(x))
    try:
        candidates.append(x.decode('utf-8'))
    except:
        pass
    candidates.append(ctf_hash(x))

print("Total candidates generated:", len(candidates))

# Test against submit API
# First make sure shahed is selected
session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "shahed"})

for cand in candidates:
    flag = cand if cand.startswith("YEK{") else f"YEK{{{cand}}}"
    try:
        r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag})
        res = r.json()
        if res.get("correct"):
            print(f"!!! SUCCESS FOR SHAHED: {flag} -> {res}")
            break
        elif "زیادی تند" in res.get("error", ""):
            import time
            time.sleep(11)
            r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag})
            res = r.json()
            if res.get("correct"):
                print(f"!!! SUCCESS FOR SHAHED: {flag} -> {res}")
                break
    except Exception as e:
        print("Error:", e)
else:
    print("Direct candidates did not match.")
