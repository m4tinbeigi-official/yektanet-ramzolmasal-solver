import hashlib
import requests
import http.cookiejar

def solve_khiar(cookie_path="cookies.txt", phone_override=None):
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_path)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

    # 1. Fetch user info
    me = session.get("https://256.yektanet.tech/ramzolmasal/api/me").json()
    user_id = me.get("id")
    masked_phone = me.get("masked_phone")
    print(f"User ID: {user_id} | Masked Phone: {masked_phone}")

    phone = phone_override or "09127047813"

    # Proverb logic: "هرچه بگندد نمکش می‌زنند"
    # Salt = user_id, value = phone
    flag_hash = hashlib.sha256(f"{phone}{user_id}".encode()).hexdigest()
    flag = f"YEK{{{flag_hash}}}"
    print(f"Computed Khiar Flag: {flag}")

    # 2. Select and Submit
    session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "khiar"})
    res = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}).json()
    print(f"Submit Result: {res}")
    return flag

if __name__ == "__main__":
    solve_khiar()
