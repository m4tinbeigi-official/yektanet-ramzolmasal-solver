import json
import hashlib
import base64

with open("/Users/ricksabchez/workspace/kimiagar_messages.json", "r") as f:
    msgs = json.load(f)

unique_words = list(set(msgs))
print(f"Total unique words for Main Account: {len(unique_words)}")

gold_words = []
for w in unique_words:
    h_bytes = hashlib.sha256(w.encode('utf-8')).digest()
    h_b64 = base64.b64encode(h_bytes).decode('utf-8')
    if h_b64.startswith("Au"):
        gold_words.append(w)

print(f"\n🥇 Found {len(gold_words)} gold words (starting with Au in base64):")
sorted_gold = sorted(gold_words)
for gw in sorted_gold:
    print(f"  - {gw}")

flag_body = "".join(sorted_gold)
flag = f"YEK{{{flag_body}}}"
print(f"\n🚩 Generated Flag for Main Account:\n{flag}")

# Also test with hex / other encodings just in case
