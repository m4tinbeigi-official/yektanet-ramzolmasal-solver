import hashlib
import re
import requests
import http.cookiejar

# Salt mining for Khiar
# The server checks if md5(salt + phone) or md5(phone + salt) matches 0e[0-9]+ (PHP Magic Hash)
# Or maybe the salt string itself is the flag!

phones = ["09127047813", "9127047813", "+989127047813"]
magic_pattern = re.compile(r'^0e[0-9]+$')

print("Mining Magic Salt for phone numbers...")

found_salts = []

for phone in phones:
    print(f"Mining for {phone}...")
    # 1. Mine salt after phone: md5(phone + salt) == 0e\d+
    for i in range(10000000):
        salt = str(i)
        h = hashlib.md5((phone + salt).encode('utf-8')).hexdigest()
        if magic_pattern.match(h):
            print(f"🎉 FOUND MAGIC SALT AFTER: phone='{phone}', salt='{salt}', md5='{h}'")
            found_salts.append((phone, salt, h, f"phone+salt"))
            if len(found_salts) >= 3:
                break

for phone in phones:
    # 2. Mine salt before phone: md5(salt + phone) == 0e\d+
    for i in range(10000000):
        salt = str(i)
        h = hashlib.md5((salt + phone).encode('utf-8')).hexdigest()
        if magic_pattern.match(h):
            print(f"🎉 FOUND MAGIC SALT BEFORE: phone='{phone}', salt='{salt}', md5='{h}'")
            found_salts.append((phone, salt, h, f"salt+phone"))
            if len(found_salts) >= 6:
                break

print("\nSummary of Found Magic Salts:", found_salts)
