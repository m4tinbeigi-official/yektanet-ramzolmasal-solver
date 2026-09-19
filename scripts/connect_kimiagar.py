import asyncio
import websockets
import ssl
import json
import http.cookiejar

cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)

cookies_header = "; ".join([f"{c.name}={c.value}" for c in cj])

async def connect_kimiagar():
    uri = "wss://256.yektanet.tech/ramzolmasal/api/kimiagar"
    extra_headers = {
        "Cookie": cookies_header,
        "User-Agent": "Mozilla/5.0",
        "Origin": "https://256.yektanet.tech",
    }
    
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    
    print(f"Connecting to: {uri}")
    
    try:
        async with websockets.connect(uri, extra_headers=extra_headers, ssl=ssl_ctx, max_size=10_000_000) as ws:
            print("Connected! Receiving messages...")
            
            messages = []
            au_messages = []
            
            for i in range(600):
                try:
                    msg = await asyncio.wait_for(ws.recv(), timeout=15)
                    
                    try:
                        parsed = json.loads(msg)
                    except:
                        parsed = msg
                    
                    messages.append(parsed)
                    
                    # Check for gold / Au
                    msg_str = str(parsed).lower()
                    if 'au' in msg_str or 'gold' in msg_str or 'طلا' in msg_str:
                        au_messages.append((i, parsed))
                        print(f"[AU FOUND at index {i}]: {str(parsed)[:200]}")
                    
                    if (i+1) % 50 == 0:
                        print(f"Received {i+1} messages so far...")
                        if messages:
                            print(f"  Sample: {str(messages[-1])[:100]}")
                
                except asyncio.TimeoutError:
                    print(f"Timeout after {i} messages")
                    break
            
            print(f"\n=== SUMMARY ===")
            print(f"Total messages received: {len(messages)}")
            print(f"AU/Gold messages: {len(au_messages)}")
            if au_messages:
                for idx, m in au_messages:
                    print(f"  [{idx}] {m}")
            
            if messages:
                print(f"\nFirst 3 messages:")
                for m in messages[:3]:
                    print(" ", str(m)[:200])
                print(f"\nLast 3 messages:")
                for m in messages[-3:]:
                    print(" ", str(m)[:200])
    
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

asyncio.run(connect_kimiagar())
