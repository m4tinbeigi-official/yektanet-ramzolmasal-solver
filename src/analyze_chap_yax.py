with open('/Users/ricksabchez/workspace/chap.bin', 'rb') as f:
    data = f.read()

print("Length of chap.bin:", len(data))
print("First 64 bytes (hex):", data[:64].hex())
print("First 64 bytes (raw):", data[:64])

# A standard WAV header starts with b'RIFF....WAVEfmt '
# The first 4 bytes of WAV are b'RIFF' = 0x52 0x49 0x46 0x46
riff = b'RIFF'
key_guess = bytes([data[i] ^ riff[i] for i in range(4)])
print("Key guess if target is RIFF:", key_guess, "hex:", key_guess.hex())

# What if key repeats?
# Or what if target is MP3 (0xFF 0xFB) or OGG (b'OggS') or FLAC (b'fLaC')?
for magic, name in [(b'RIFF', 'WAV/RIFF'), (b'OggS', 'OGG'), (b'fLaC', 'FLAC'), (b'ID3', 'MP3 ID3'), (b'\xff\xfb', 'MP3 Frame')]:
    k = bytes([data[i] ^ magic[i] for i in range(len(magic))])
    print(f"Key if {name}: {k} (hex: {k.hex()})")
