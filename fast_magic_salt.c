#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <CommonCrypto/CommonDigest.h>

int is_magic_hash(const unsigned char *digest) {
    // Check if starts with 0e and rest are all decimal digits
    // In hex: digest[0] == 0x0e
    if (digest[0] != 0x0e) return 0;
    for (int i = 1; i < 16; i++) {
        uint8_t hi = (digest[i] >> 4) & 0x0f;
        uint8_t lo = digest[i] & 0x0f;
        if (hi > 9 || lo > 9) return 0;
    }
    return 1;
}

int main(int argc, char **argv) {
    const char *phones[] = {"09127047813", "9127047813", "+989127047813"};
    char buf[128];
    unsigned char digest[16];

    for (int p_idx = 0; p_idx < 3; p_idx++) {
        const char *phone = phones[p_idx];
        printf("Mining for phone: %s (after)...\n", phone);
        for (uint64_t i = 0; i < 500000000ULL; i++) {
            int len = sprintf(buf, "%s%llu", phone, i);
            CC_MD5(buf, len, digest);
            if (is_magic_hash(digest)) {
                printf("🎉 FOUND MAGIC SALT AFTER: phone='%s', salt='%llu', hex=", phone, i);
                for (int j = 0; j < 16; j++) printf("%02x", digest[j]);
                printf("\n");
                break;
            }
        }

        printf("Mining for phone: %s (before)...\n", phone);
        for (uint64_t i = 0; i < 500000000ULL; i++) {
            int len = sprintf(buf, "%llu%s", i, phone);
            CC_MD5(buf, len, digest);
            if (is_magic_hash(digest)) {
                printf("🎉 FOUND MAGIC SALT BEFORE: phone='%s', salt='%llu', hex=", phone, i);
                for (int j = 0; j < 16; j++) printf("%02x", digest[j]);
                printf("\n");
                break;
            }
        }
    }
    return 0;
}
