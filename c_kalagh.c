#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
#include <curl/curl.h>

uint32_t fnv1a(const char *str, size_t len) {
    uint32_t h = 2166136261U;
    for (size_t i = 0; i < len; i++) {
        h = (h ^ (uint8_t)str[i]) * 16777619U;
    }
    return h;
}

uint64_t find_nonce(const char *payam) {
    char buf[128];
    uint64_t nonce = 0;
    while (1) {
        int len = sprintf(buf, "%s:%llu", payam, nonce);
        uint32_t h = fnv1a(buf, len);
        if (h < 2048) {
            return nonce;
        }
        nonce++;
    }
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
    if (argc < 2) {
        printf("Usage: %s <cookie_file>\n", argv[0]);
        return 1;
    }
    const char *cookie_file = argv[1];
    
    CURL *curl = curl_easy_init();
    if (!curl) return 1;

    struct curl_slist *headers = NULL;
    headers = curl_slist_append(headers, "Content-Type: application/json");

    curl_easy_setopt(curl, CURLOPT_COOKIEFILE, cookie_file);
    curl_easy_setopt(curl, CURLOPT_COOKIEJAR, cookie_file);
    curl_easy_setopt(curl, CURLOPT_HTTPHEADER, headers);

    // Initial GET
    struct MemoryStruct chunk;
    chunk.memory = malloc(1);
    chunk.size = 0;

    curl_easy_setopt(curl, CURLOPT_URL, "https://256.yektanet.tech/ramzolmasal/api/kalagh");
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, (void *)&chunk);
    curl_easy_setopt(curl, CURLOPT_HTTPGET, 1L);

    CURLcode res = curl_easy_perform(curl);
    printf("Initial response: %s\n", chunk.memory);

    for (int step = 0; step < 200; step++) {
        if (strstr(chunk.memory, "YEK{") != NULL || strstr(chunk.memory, "flag") != NULL) {
            printf("\n\n>>> FOUND FLAG: %s <<<\n\n", chunk.memory);
            break;
        }

        // extract shomare and payam
        char *shomare_pos = strstr(chunk.memory, "\"shomare\":");
        char *payam_pos = strstr(chunk.memory, "\"payam\":\"");
        if (!shomare_pos || !payam_pos) {
            printf("Finished or format unrecognized: %s\n", chunk.memory);
            break;
        }

        int shomare = atoi(shomare_pos + 10);
        char payam[128] = {0};
        char *payam_start = payam_pos + 9;
        char *payam_end = strchr(payam_start, '"');
        if (!payam_end) break;
        strncpy(payam, payam_start, payam_end - payam_start);

        uint64_t nonce = find_nonce(payam);
        printf("Step %d (kalagh %d): payam=%s nonce=%llu\n", step + 1, shomare, payam, nonce);

        char post_data[256];
        sprintf(post_data, "{\"shomare\":%d,\"nonce\":\"%llu\"}", shomare, nonce);

        free(chunk.memory);
        chunk.memory = malloc(1);
        chunk.size = 0;

        curl_easy_setopt(curl, CURLOPT_POSTFIELDS, post_data);
        curl_easy_perform(curl);
        printf("-> Server: %s\n", chunk.memory);
    }

    curl_easy_cleanup(curl);
    return 0;
}
