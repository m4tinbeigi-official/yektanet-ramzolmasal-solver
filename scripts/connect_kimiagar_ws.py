import websocket
import ssl
import json
import http.cookiejar

cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)

cookie_str = "; ".join([f"{c.name}={c.value}" for c in cj])
print("Using cookie:", cookie_str)

ws_urls = [
    "wss://256.yektanet.tech/ramzolmasal/ws",
    "wss://256.yektanet.tech/ramzolmasal/api/ws",
    "wss://256.yektanet.tech/ramzolmasal/socket",
    "wss://256.yektanet.tech/ramzolmasal/kimiagar",
    "wss://256.yektanet.tech/ramzolmasal/api/kimiagar",
    "wss://256.yektanet.tech/ws",
    "wss://256.yektanet.tech/socket",
]

for url in ws_urls:
    try:
        print(f"Trying WS {url}...")
        ws = websocket.create_connection(
            url,
            timeout=5,
            sslopt={"cert_reqs": ssl.CERT_NONE},
            header=[
                f"Cookie: {cookie_str}",
                "User-Agent: Mozilla/5.0",
                "Origin: https://256.yektanet.tech"
            ]
        )
        print(f"🎉🎉🎉 SUCCESS CONNECTED TO WS: {url} 🎉🎉🎉")
        # Listen for messages
        for _ in range(5):
            msg = ws.recv()
            print("  Received WS Message:", msg)
        ws.close()
    except Exception as e:
        # print error
        pass

print("WS test done.")
