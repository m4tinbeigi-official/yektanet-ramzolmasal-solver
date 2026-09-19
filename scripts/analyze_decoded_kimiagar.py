with open("/Users/ricksabchez/workspace/kimiagar_messages.json", "r") as f:
    import json
    msgs = json.load(f)

header = msgs[:64]
body = msgs[64:]
b64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
token_to_b64 = {token: b64_alphabet[i] for i, token in enumerate(header)}
b64_string = "".join([token_to_b64[t] for t in body])

import base64
raw_bytes = base64.b64decode(b64_string)

print("Hex representation:")
print(raw_bytes.hex())

# Test XOR with common keys
keys = [b"Au", b"AU", b"au", b"gold", b"Gold", b"GOLD", b"kimiagar", b"YEK", b"256"]

for k in keys:
    x = bytes([raw_bytes[i] ^ k[i % len(k)] for i in range(len(raw_bytes))])
    text = x.decode('utf-8', errors='ignore')
    if "YEK" in text or "flag" in text.lower() or "طلا" in text or "زر" in text:
        print(f"\n🎉 FOUND WITH KEY {k}:")
        print(text)
