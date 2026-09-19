import requests
import http.cookiejar

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

print("Checking level pelak status...")
r_st = session.get("https://256.yektanet.tech/ramzolmasal/api/status?level=pelak")
print("Status pelak:", r_st.status_code, r_st.text)

# Check custom endpoints for pelak
for ep in [
    "api/pelak", "api/khaneh", "api/home", "api/neighbors", "api/divar",
    "api/divar-be-divar", "api/plaque", "api/house", "api/files/pelak.txt"
]:
    r = session.get(f"https://256.yektanet.tech/ramzolmasal/{ep}")
    if r.status_code != 404:
        print(f"Found endpoint {ep} -> {r.status_code}: {r.text[:200]}")
