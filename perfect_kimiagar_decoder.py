import json
import base64

with open("/Users/ricksabchez/workspace/kimiagar_messages.json", "r") as f:
    msgs = json.load(f)

# The first 64 messages are the mapping!
header = msgs[:64]
body = msgs[64:]

print(f"Header length: {len(header)} (Unique: {len(set(header))})")
print(f"Body length: {len(body)}")

# Standard Base64 alphabet: A-Z, a-z, 0-9, +, /
b64_alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"

# Create mapping dictionary
token_to_b64 = {token: b64_alphabet[i] for i, token in enumerate(header)}

# Decode body
b64_string = "".join([token_to_b64[t] for t in body])
print(f"\nConstructed Base64 string (len={len(b64_string)}):\n{b64_string}")

# Base64 decode
try:
    decoded_bytes = base64.b64decode(b64_string)
    print(f"\nDecoded bytes length: {len(decoded_bytes)}")
    print(f"Decoded string (utf-8):")
    print(decoded_bytes.decode('utf-8', errors='replace'))
    
    # Let's save to file
    with open("/Users/ricksabchez/workspace/kimiagar_decoded.txt", "w") as f:
        f.write(decoded_bytes.decode('utf-8', errors='replace'))
except Exception as e:
    print(f"Decoding error: {e}")
