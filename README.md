# stupid-csv-tricks
Code for doing slightly atypical things with CSVs

## csv_gen

Randomly generates CSVs. The first column is a binary classification and
the rest of the columns are doubles. Generated CSVs have headers.

csv_gen is *cute*: it formats numbers so that the size of the CSV on-disk is
the same as the size of an equivalent array of doubles in memory. For example, 
a 1GB CSV on disk will become a 1GB Numpy array if it is loaded into Numpy.

### Building

    $ gcc -O2 -o csv_gen csv_gen.c

### Usage

    $ ./csv_gen NUM_ROWS NUM_COLS

CSVs are written to standard out

### Example

    $ ./csv_gen 512 256 > MB.csv

## csv_to_npy

Converts A CSV of doubles with a header to a file in Numpy's 
[".npy" format](http://docs.scipy.org/doc/numpy-dev/neps/npy-format.html).

### Building

    $ gcc -O2 -o csv_to_npy csv_to_npy.c

### Usage

    $ ./csv_to_npy CSV_FILE

.npy files are written to standard out

### Example

    $ ./csv_to_npy MB.csv > MB.npy
    $ python -c 'from numpy import load; a = load("MB.npy"); print a.shape'
    (512, 256)

## csv_to_rst.py

Converts a CSV with a header to 
[RST grid-format tables](http://docutils.sourceforge.net/docs/user/rst/quickref.html#tables).

### Usage

    $ python csv_to_rst.py

csv_to_rst.py takes csvs from standard in and writes rst tables to stdout

### Example

    $ echo -e 'idx,name,title\n1,Jim,CEO\n2,Bill,Engineer' | python csv_to_rst.py 
    +-----+------+----------+
    | idx | name |    title |
    +=====+======+==========+
    |   1 |  Jim |      CEO |
    +-----+------+----------+
    |   2 | Bill | Engineer |
    +-----+------+----------+ 

## csv_to_sqlite.py

Converts a CSV with a header to an sqlite database. Requires 
[diogenes](https://github.com/dssg/diogenes).

### Usage

    $ python csv_to_sqlite.py [-h] [--sqlite_path SQLITE_PATH]
                        [--table_name TABLE_NAME]
                        csv_path

* SQLITE_PATH is the path to the sqlite database to produce
* TABLE_NAME is the name of the table into which the CSV will be dumped
* csv_path is the path to the csv file

### Example

    $ python csv_to_sqlite.py --sqlite_path MB.db --table_name MB MB.csv
    written to file: MB.db, table: "MB" 
