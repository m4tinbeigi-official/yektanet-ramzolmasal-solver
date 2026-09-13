#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <pthread.h>
#include <CommonCrypto/CommonDigest.h>

#define NUM_THREADS 8

typedef struct {
    const char *prefix;
    uint64_t start_i;
    uint64_t step;
    volatile int *found;
    uint64_t *result_nonce;
    unsigned char result_digest[16];
} Worker;

int is_magic_hash(const unsigned char *digest) {
    if (digest[0] != 0x0e) return 0;
    for (int i = 1; i < 16; i++) {
        uint8_t hi = (digest[i] >> 4) & 0x0f;
        uint8_t lo = digest[i] & 0x0f;
        if (hi > 9 || lo > 9) return 0;
    }
    return 1;
}

void *worker_fn(void *arg) {
    Worker *w = (Worker *)arg;
    char buf[128];
    unsigned char digest[16];
    uint64_t i = w->start_i;

    while (!(*(w->found))) {
        int len = sprintf(buf, "%s%llu", w->prefix, i);
        CC_MD5(buf, len, digest);
        if (is_magic_hash(digest)) {
            *(w->result_nonce) = i;
            memcpy(w->result_digest, digest, 16);
            *(w->found) = 1;
            break;
        }
        i += w->step;
    }
    return NULL;
}

int main(int argc, char **argv) {
    const char *prefixes[] = {
        "88004c9a09127047813",
        "0912704781388004c9a",
        "88004c9a:09127047813",
        "09127047813:88004c9a",
        "88004c9a9127047813",
        "912704781388004c9a"
    };

    for (int p_idx = 0; p_idx < 6; p_idx++) {
        const char *prefix = prefixes[p_idx];
        pthread_t threads[NUM_THREADS];
        Worker workers[NUM_THREADS];
        volatile int found = 0;
        uint64_t result_nonce = 0;

        for (int t = 0; t < NUM_THREADS; t++) {
            workers[t].prefix = prefix;
            workers[t].start_i = t;
            workers[t].step = NUM_THREADS;
            workers[t].found = &found;
            workers[t].result_nonce = &result_nonce;
            pthread_create(&threads[t], NULL, worker_fn, &workers[t]);
        }

        for (int t = 0; t < NUM_THREADS; t++) {
            pthread_join(threads[t], NULL);
        }

        if (found) {
            printf("🎉 FOUND MAGIC NONCE: prefix='%s', nonce=%llu, md5=", prefix, result_nonce);
            for (int j = 0; j < 16; j++) printf("%02x", workers[0].result_digest[j]);
            printf("\n");
        }
    }
    return 0;
}
