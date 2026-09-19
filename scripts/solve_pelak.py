import requests
import http.cookiejar
import hashlib

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

me = session.get("https://256.yektanet.tech/ramzolmasal/api/me").json()
print("My Info:", me)

# Charm: "همیشه شماره تلفنشو می‌چسبونه به شماره موبایلش و میشه رمزش."
# Let's inspect the icon / image in pelak for a house / phone / plaque number!
st = session.get("https://256.yektanet.tech/ramzolmasal/api/status?level=pelak").json()
icon_b64 = st.get('level', {}).get('icon')
if icon_b64 and "base64," in icon_b64:
    import base64
    raw_img = base64.b64decode(icon_b64.split("base64,")[1])
    with open("/Users/ricksabchez/workspace/pelak_icon.jpg", "wb") as f:
        f.write(raw_img)
    print(f"Saved pelak_icon.jpg ({len(raw_img)} bytes)")
