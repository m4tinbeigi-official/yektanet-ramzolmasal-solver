import requests
import http.cookiejar

session = requests.Session()
cj = http.cookiejar.MozillaCookieJar("/Users/ricksabchez/workspace/ramzolmasal_cookies.txt")
cj.load(ignore_discard=True, ignore_expires=True)
session.cookies = cj

ya_proverbs = [
    "ya-ali", "ya-rab", "ya-bakht", "ya-marg", "ya-romi", "ya-zangi",
    "ya-takht", "ya-sheykh", "ya-hagh", "ya-hoo", "ya-zahra", "ya-hosein",
    "ya-abolfazl", "ya-reza", "ya-mahdi", "ya-khoda", "ya-mohammad",
    "ya_ali", "ya_rab", "ya_bakht", "ya_marg", "ya_romi", "ya_zangi",
    "یا علی", "یا رب", "یا بخت", "یا مرگ", "یا رومی", "یا زنگی",
    "یا_علی", "یا_رب", "یا_بخت", "یا_مرگ", "یا_رومی", "یا_زنگی",
    "یا رومی رومی یا زنگی زنگی", "یا_رومی_رومی_یا_زنگی_زنگی",
    "یا مکن با پیلبانان دوستی یا بنا کن خانه ای در خورد پیل",
    "یا_مکن_با_پیلبانان_دوستی_یا_بنا_کن_خانه_ای_در_خورد_پیل",
    "یا تخت یا تخته", "یا_تخت_یا_تخته"
]

for p in ya_proverbs:
    url = f"https://256.yektanet.tech/ramzolmasal/api/status?level={p}"
    r = session.get(url)
    if r.status_code == 200:
        data = r.json()
        if data.get('level', {}).get('id') == p:
            print(f"FOUND YA-X MATCH: {p} -> {data.get('level')}")

print("Ya-X scan complete.")
