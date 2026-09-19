import json
import base64

def analyze():
    try:
        with open("/Users/ricksabchez/workspace/kimiagar_messages.json", "r") as f:
            msgs = json.load(f)
    except Exception as e:
        print(f"Error loading file: {e}")
        return
    
    print(f"Loaded {len(msgs)} messages from kimiagar.")
    
    # Check lengths
    lengths = set(len(m) for m in msgs)
    print(f"Lengths of messages: {lengths}")
    
    # Check charset
    charset = set("".join(msgs))
    print(f"Charset ({len(charset)} chars): {''.join(sorted(charset))}")
    
    # First 20
    print("\nFirst 20 items:")
    for i, m in enumerate(msgs[:20]):
        print(f"  {i+1:03d}: {m}")
        
    # Are there duplicates?
    from collections import Counter
    counts = Counter(msgs)
    print(f"\nUnique items count: {len(counts)}")
    most_common = counts.most_common(5)
    print(f"Most common items: {most_common}")

if __name__ == "__main__":
    analyze()
