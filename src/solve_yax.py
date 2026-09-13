import base64
import requests
import http.cookiejar
from PIL import Image
import io

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

st = session.get("https://256.yektanet.tech/ramzolmasal/api/status?level=ya-x").json()
icon_b64 = st['level']['icon'].split(',')[1]
img_bytes = base64.b64decode(icon_b64)

# Open image with PIL
img = Image.open(io.BytesIO(img_bytes))
print(f"Icon Image: size={img.size}, mode={img.mode}")

# Convert to RGB (3072 bytes) or RGBA (4096 bytes)
rgb_img = img.convert('RGB')
raw_pixels = rgb_img.tobytes()
print("Raw RGB pixels length:", len(raw_pixels))

with open('/Users/ricksabchez/workspace/chap.bin', 'rb') as f:
    chap_bytes = f.read()

print("Chap.bin length:", len(chap_bytes))

# XOR chap.bin with raw_pixels
xored = bytes([chap_bytes[i] ^ raw_pixels[i] for i in range(len(chap_bytes))])
print("First 32 bytes of xored:", xored[:32])

# Save output
with open('/Users/ricksabchez/workspace/sound.wav', 'wb') as f:
    f.write(xored)

print("Saved sound.wav! First 16 bytes:", xored[:16])
