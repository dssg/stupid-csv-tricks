#include <stdio.h>
#include <stdlib.h>
#include <time.h>

float random_float(void) {
    return (float)rand()/(float)(RAND_MAX);
}

void make_pdf(size_t n_rows, size_t n_cols) {
    int row;
    int col;

    srand(time(NULL));
    printf("f0");
    for (col = 1; col < n_cols; ++col) {
        printf(",f%d", col);
    }
    // Notice we're being cute and making the size of the csv on disk
    // almost the same size as an array of doubles in memory
    printf("\n");
    for (row = 0; row < n_rows; ++row) {
        // The first column is the label, so we make it binary
        printf("%08d", rand() % 2);
        for (col = 1; col < n_cols; ++col) {
            printf(",%1.5f", random_float());
        }
        printf("\n");
    }
}

int main(int argc, char *argv[]) {
    if (argc >= 3) {
        size_t n_rows = atoi(argv[1]);
        size_t n_cols = atoi(argv[2]);
        make_pdf(n_rows, n_cols);
    }
}


