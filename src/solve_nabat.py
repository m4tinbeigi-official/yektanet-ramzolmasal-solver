import requests
import http.cookiejar

def solve_nabat(cookie_path="cookies.txt", product="نبات"):
    session = requests.Session()
    cj = http.cookiejar.MozillaCookieJar(cookie_path)
    cj.load(ignore_discard=True, ignore_expires=True)
    session.cookies = cj

    # Based on robots.txt and proverb: "خر چه داند قیمت نقل و نبات"
    headers = {
        "User-Agent": "khar"
    }

    url = "https://256.yektanet.tech/ramzolmasal/api/price"
    r = session.get(url, params={"product_name": product}, headers=headers)
    data = r.json()
    print("Response:", data)

    price = data.get("price")
    if price:
        flag = f"YEK{{{price}}}"
        print(f"Submitting flag for nabat: {flag}")
        session.post("https://256.yektanet.tech/ramzolmasal/api/select", json={"id": "nabat"})
        res = session.post("https://256.yektanet.tech/ramzolmasal/api/submit", json={"flag": flag}).json()
        print("Submit result:", res)
        return price
    else:
        print("Failed to extract price:", data)

if __name__ == "__main__":
    solve_nabat()
