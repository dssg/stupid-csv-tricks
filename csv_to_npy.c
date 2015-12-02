#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "csv_to_npy.h"


void csv_to_npy(FILE *f_csv, FILE *f_npy) {
    size_t n_cols = 1;
    size_t n_rows = 0;
    double cell;
    char c;

    /* First pass -- get number of cols and rows */

    // count commas in first row to get columns
    while ((c = fgetc(f_csv)) != (int)'\n') {
        if (c == (int)',') {
            ++n_cols;
        }
    }

    // count rows (that aren't blank)
    while (1) {
        if (fscanf(f_csv, "%lf", &cell) > 0) {
            //This row has data in it
            ++n_rows;
        } 
        //fast forward to next newline
        while ((c = fgetc(f_csv)) != (int)'\n');
        if ((c = fgetc(f_csv)) == EOF) {
            break;
        }
        ungetc(c, f_csv);
    }



    //print header
    char header[NPY_HEADER_LEN + 1];
    sprintf(header, NPY_HEADER, n_rows, n_cols);
    header[7] = 0;
    header[9] = 0;
    fwrite(header, 1, NPY_HEADER_LEN, f_npy);

    /* Second pass. */
    rewind(f_csv);
    // skip the header row
    while ((c = fgetc(f_csv)) != (int)'\n');

    size_t n_cells = n_rows * n_cols;
    size_t cell_ind;
    double cell_val;
    for (cell_ind = 0; cell_ind < n_cells; ++cell_ind) {
        fscanf(f_csv, "  %lf %*[,] ", &cell_val);
        //fwrite(&cell_val, 1, sizeof(cell_val), f_npy);
    }    

}

void usage(void) {
    exit(0);
}

int main(int argc, char *argv[]) {
    FILE *f_csv;
    FILE *f_npy;
    if (argc < 2) {
        usage();
    }
    f_csv = fopen(argv[1], "r");
    if (argc > 2) {
        f_npy = fopen(argv[2], "w");
    } else {
        f_npy = stdout;
    }
    csv_to_npy(f_csv, f_npy);
    fclose(f_csv);
    if (argc > 2) {
        fclose(f_npy);
    }
    return 0;
}
