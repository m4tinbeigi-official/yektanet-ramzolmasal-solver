#include <stdio.h>
#include <string.h>
#include <stdint.h>
#include <stdlib.h>
#include <pthread.h>
#include <CommonCrypto/CommonDigest.h>

#define NUM_THREADS 8

typedef struct {
    const char *phone;
    int is_prefix; // 1 if salt + phone, 0 if phone + salt
    uint64_t start_i;
    uint64_t step;
    volatile int *found;
    uint64_t *result_salt;
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
        int len;
        if (w->is_prefix) {
            len = sprintf(buf, "%llu%s", i, w->phone);
        } else {
            len = sprintf(buf, "%s%llu", w->phone, i);
        }
        CC_MD5(buf, len, digest);
        if (is_magic_hash(digest)) {
            *(w->result_salt) = i;
            memcpy(w->result_digest, digest, 16);
            *(w->found) = 1;
            break;
        }
        i += w->step;
    }
    return NULL;
}

int main(int argc, char **argv) {
    const char *phone = "09127047813";
    if (argc > 1) phone = argv[1];

    printf("Multi-threaded Mining for phone: %s ...\n", phone);

    for (int is_prefix = 0; is_prefix <= 1; is_prefix++) {
        pthread_t threads[NUM_THREADS];
        Worker workers[NUM_THREADS];
        volatile int found = 0;
        uint64_t result_salt = 0;

        for (int t = 0; t < NUM_THREADS; t++) {
            workers[t].phone = phone;
            workers[t].is_prefix = is_prefix;
            workers[t].start_i = t;
            workers[t].step = NUM_THREADS;
            workers[t].found = &found;
            workers[t].result_salt = &result_salt;
            pthread_create(&threads[t], NULL, worker_fn, &workers[t]);
        }

        for (int t = 0; t < NUM_THREADS; t++) {
            pthread_join(threads[t], NULL);
        }

        if (found) {
            printf("🎉 FOUND (%s): Salt = %llu | Hash = ", is_prefix ? "salt+phone" : "phone+salt", result_salt);
            for (int j = 0; j < 16; j++) printf("%02x", workers[0].result_digest[j]);
            printf("\n");
        }
    }
    return 0;
}
