#!/usr/bin/env python

import csv
import sys

def csv_to_rst(fin, fout):
    rows = [row for row in csv.reader(fin)]
    col_widths = [max([len(cell) for cell in col]) for col in zip(*rows)]
    fmt = '{sep}' + '{sep}'.join(
            ['{{space}}{{{idx}:>{width}}}{{space}}'.format(
                idx=idx, 
                width=width) for idx, width in 
             enumerate(col_widths)]) + '{sep}\n'
    boundary = fmt.format(
            *['-' * width for width in col_widths],
            sep='+',
            space='-')
    header_boundary = boundary.replace('-', '=')

    fout.write(boundary)
    fout.write(fmt.format(
            *rows[0],
            sep='|',
            space=' '))
    fout.write(header_boundary)

    for row in rows[1:]:
        fout.write(fmt.format(
            *row,
            sep='|',
            space=' '))
        fout.write(boundary)

if __name__ == '__main__':
    csv_to_rst(sys.stdin, sys.stdout)
