import base64
import requests
import http.cookiejar
import xml.etree.ElementTree as ET

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

st = session.get("https://256.yektanet.tech/ramzolmasal/api/status?level=sargijeh").json()
bg = st['level']['background']
svg_data = base64.b64decode(bg.split(',')[1]).decode('utf-8')

with open("/Users/ricksabchez/workspace/sargijeh.svg", "w") as f:
    f.write(svg_data)

print("Saved SVG! Length:", len(svg_data))
