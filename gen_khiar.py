import hashlib
import requests
import http.cookiejar

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})

phones = ["09127047813", "9127047813", "+989127047813", "0912***7813", "88004c9a"]
salts = [
    "namak", "khiar", "khiarshoor", "khiar_shoor", "khiarshur", "namakzar", "salt",
    "نمک", "خیار", "خیارشور", "خیار_شور", "بانمک", "شور", "نمکستان"
]

candidates = []

# Proverb phrases
candidates.extend([
    "خیارشور", "خیار_شور", "خیار شور", "khiarshoor", "khiar_shoor", "khiarshur", "khiar_shur",
    "نمک", "namak", "salt", "salted", "salted_cucumber", "pickle", "pickles",
    "هر چه بگندد نمکش می زنند", "هر_چه_بگندد_نمکش_می_زنند",
    "هرچه بگندد نمکش می زنند", "هرچه_بگندد_نمکش_می_زنند",
    "هر چه بگندد نمکش میزنند", "هر_چه_بگندد_نمکش_میزنند",
    "هرچه بگندد نمکش میزنند", "هرچه_بگندد_نمکش_میزنند",
    "وای به روزی که بگندد نمک", "وای_به_روزی_که_بگندد_نمک",
])

# Phone hashes with salt
for p in phones:
    for s in salts:
        # SHA256
        h1 = hashlib.sha256(f"{p}:{s}".encode()).hexdigest()
        h2 = hashlib.sha256(f"{p}{s}".encode()).hexdigest()
        h3 = hashlib.sha256(f"{s}:{p}".encode()).hexdigest()
        h4 = hashlib.sha256(f"{s}{p}".encode()).hexdigest()
        candidates.extend([h1, h2, h3, h4])
        # MD5
        m1 = hashlib.md5(f"{p}:{s}".encode()).hexdigest()
        m2 = hashlib.md5(f"{p}{s}".encode()).hexdigest()
        candidates.extend([m1, m2])

print(f"Total candidates for Khiar: {len(candidates)}")

with open('/Users/ricksabchez/workspace/khiar_candidates.txt', 'w') as f:
    for c in candidates:
        f.write(c + '\n')
