import asyncio
import websockets
import ssl
import hashlib
import base64
import json
import http.cookiejar
import requests
import time

ACCOUNTS = [
    ("متین بیگی (m4tinbeigi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies.txt"),
    ("ریک سانچز (Rick Sanchez)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_rick.txt"),
    ("یگانه بیگی (Yeganeh)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_yeganeh.txt"),
    ("تیم ابراهیمی (Ebrahimi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_ebrahimi.txt"),
]

async def solve_kimiagar_account(name, cookie_path):
    print(f"\n=======================================================")
    print(f"⚗️ حل مرحله کیمیاگر برای: {name}")
    print(f"=======================================================")
    
    cj = http.cookiejar.MozillaCookieJar(cookie_path)
    cj.load(ignore_discard=True, ignore_expires=True)
    cookies_header = "; ".join([f"{c.name}={c.value}" for c in cj])
    
    uri = "wss://256.yektanet.tech/ramzolmasal/api/kimiagar"
    ssl_ctx = ssl.create_default_context()
    ssl_ctx.check_hostname = False
    ssl_ctx.verify_mode = ssl.CERT_NONE
    
    headers = {
        "Cookie": cookies_header,
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
        "Origin": "https://256.yektanet.tech",
    }
    
    print("🔹 در حال اتصال به وب‌سوکت کارگاه کیمیاگر...")
    messages = []
    async with websockets.connect(uri, ssl=ssl_ctx, additional_headers=headers, max_size=10_000_000) as ws:
        for _ in range(650):
            try:
                msg = await asyncio.wait_for(ws.recv(), timeout=2.5)
                messages.append(msg)
            except Exception:
                break
                
    print(f"  📥 دریافت {len(messages)} پیام از وب‌سوکت.")
    unique_words = list(set(messages))
    print(f"  ✨ تعداد کلمات یکتا: {len(unique_words)}")
    
    # Filter gold words (SHA-256 in Base64 starts with 'Au')
    gold_words = []
    for w in unique_words:
        h_bytes = hashlib.sha256(w.encode('utf-8')).digest()
        h_b64 = base64.b64encode(h_bytes).decode('utf-8')
        if h_b64.startswith("Au"):
            gold_words.append(w)
            
    print(f"  🥇 تعداد کلمات طلایی غربال‌شده (شروع با Au): {len(gold_words)}")
    sorted_gold = sorted(gold_words)
    print(f"  📋 کلمات طلایی مرتب‌شده: {sorted_gold}")
    
    flag_body = "".join(sorted_gold)
    flag = f"YEK{{{flag_body}}}"
    print(f"  🚩 پرچم تولیدشده: {flag}")
    
    # Submit flag via HTTP Session
    session = requests.Session()
    session.cookies = cj
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "kimiagar"})
    time.sleep(1)
    
    while True:
        r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}).json()
        if "زیادی تند" in r.get("error", ""):
            time.sleep(6)
            continue
        if r.get("correct"):
            print(f"  🎉🎉🎉 موفقیت! مرحله کیمیاگر برای {name} حل و ثبت شد! ({r.get('message')})")
        else:
            print(f"  نتیجه سابمیت: {r}")
        break
    time.sleep(10.5)

async def main():
    for name, path in ACCOUNTS:
        await solve_kimiagar_account(name, path)

if __name__ == "__main__":
    asyncio.run(main())
