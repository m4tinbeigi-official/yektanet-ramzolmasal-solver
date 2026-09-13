#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>

uint32_t fnv1a(const char *str, size_t len) {
    uint32_t h = 2166136261U;
    for (size_t i = 0; i < len; i++) {
        h = (h ^ (uint8_t)str[i]) * 16777619U;
    }
    return h;
}

int main(int argc, char **argv) {
    if (argc < 2) return 1;
    const char *payam = argv[1];
    char buf[128];
    uint64_t nonce = 0;
    
    while (1) {
        int len = sprintf(buf, "%s:%llu", payam, nonce);
        uint32_t h = fnv1a(buf, len);
        if (h < 2048) {
            printf("%llu\n", nonce);
            return 0;
        }
        nonce++;
    }
    return 0;
}
