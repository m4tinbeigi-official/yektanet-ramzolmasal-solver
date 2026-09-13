#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <curl/curl.h>

#define NUM_THREADS 10

uint32_t fnv1a(const char *str, size_t len) {
    uint32_t h = 2166136261U;
    for (size_t i = 0; i < len; i++) {
        h = (h ^ (uint8_t)str[i]) * 16777619U;
    }
    return h;
}

typedef struct {
    const char *payam;
    uint64_t start_nonce;
    uint64_t step;
    volatile int *found;
    uint64_t *result_nonce;
} WorkerArg;

void *worker_fn(void *arg) {
    WorkerArg *w = (WorkerArg *)arg;
    char buf[128];
    uint64_t nonce = w->start_nonce;
    while (!(*(w->found))) {
        int len = sprintf(buf, "%s:%llu", w->payam, nonce);
        uint32_t h = fnv1a(buf, len);
        if (h < 2048) {
            *(w->result_nonce) = nonce;
            *(w->found) = 1;
            break;
        }
        nonce += w->step;
    }
    return NULL;
}

uint64_t find_nonce_mt(const char *payam) {
    pthread_t threads[NUM_THREADS];
    WorkerArg args[NUM_THREADS];
    volatile int found = 0;
    uint64_t result_nonce = 0;

    for (int i = 0; i < NUM_THREADS; i++) {
        args[i].payam = payam;
        args[i].start_nonce = i;
        args[i].step = NUM_THREADS;
        args[i].found = &found;
        args[i].result_nonce = &result_nonce;
        pthread_create(&threads[i], NULL, worker_fn, &args[i]);
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        pthread_join(threads[i], NULL);
    }
    return result_nonce;
}

struct MemoryStruct {
    char *memory;
    size_t size;
};

static size_t WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp) {
    size_t realsize = size * nmemb;
    struct MemoryStruct *mem = (struct MemoryStruct *)userp;
    char *ptr = realloc(mem->memory, mem->size + realsize + 1);
    if (!ptr) return 0;
    mem->memory = ptr;
    memcpy(&(mem->memory[mem->size]), contents, realsize);
    mem->size += realsize;
    mem->memory[mem->size] = 0;
    return realsize;
}

int main(int argc, char **argv) {
    setvbuf(stdout, NULL, _IONBF, 0);
    if (argc < 2) return 1;
    const char *cookie_file = argv[1];

    CURL *curl = curl_easy_init();
    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_COOKIEFILE, cookie_file);
    curl_easy_setopt(curl, CURLOPT_COOKIEJAR, cookie_file);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    struct MemoryStruct chunk;
    chunk.memory = malloc(1);
    chunk.size = 0;

    curl_easy_setopt(curl, CURLOPT_URL, "https://256.yektanet.tech/ramzolmasal/api/kalagh");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);
    curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);

    curl_easy_perform(curl);

    for (int step = 0; step < 300; step++) {
        if (strstr(chunk.memory, "YEK{") != NULL || strstr(chunk.memory, "flag") != NULL) {
            printf("\n\n>>> FINAL KALAGH FLAG: %s <<<\n\n", chunk.memory);
            break;
        }

        char *shomare_pos = strstr(chunk.memory, "\"shomare\":");
        char *payam_pos = strstr(chunk.memory, "\"payam\":\"");
        if (!shomare_pos || !payam_pos) {
            printf("Ended: %s\n", chunk.memory);
            break;
        }

        int shomare = atoi(shomare_pos + 10);
        char payam[128] = {0};
        char *payam_start = payam_pos + 9;
        char *payam_end = strchr(payam_start, '"');
        if (!payam_end) break;
        strncpy(payam, payam_start, payam_end - payam_start);

        uint64_t nonce = find_nonce_mt(payam);
        if (shomare % 25 == 0 || shomare > 250) {
            printf("[%d] shomare: %d | nonce: %llu\n", step + 1, shomare, nonce);
        }

        char post_data[256];
        sprintf(post_data, "{\"shomare\":%d,\"nonce\":\"%llu\"}", shomare, nonce);

        free(chunk.memory);
        chunk.memory = malloc(1);
        chunk.size = 0;

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data);
        curl_easy_perform(curl);
    }

    curl_easy_cleanup(curl);
    return 0;
}
