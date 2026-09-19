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

# Let's test single-byte XOR keys (0 to 255)
print("=== Scanning single-byte XOR keys on 402 bytes ===")
for k in range(256):
    xored = bytes([b ^ k for b in raw_bytes])
    try:
        text = xored.decode('utf-8')
        if "YEK" in text or "flag" in text.lower() or "طلا" in text or "زر" in text or "مس" in text:
            print(f"\n🎉 FOUND UTF-8 WITH BYTE KEY {k} (0x{k:02x}):")
            print(text)
    except:
        pass

# Also look for ascii / latin1 readable substrings
for k in range(256):
    xored = bytes([b ^ k for b in raw_bytes])
    text = xored.decode('latin1')
    if "YEK{" in text or "flag{" in text.lower():
        print(f"\n🎉 FOUND ASCII FLAG WITH BYTE KEY {k} (0x{k:02x}):")
        print(text[:100])
