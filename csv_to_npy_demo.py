#!/usr/bin/env python

import os

import numpy as np

# compile
os.system('gcc -o csv_to_npy csv_to_npy.c')

# make a test csv
with open('test.csv', 'w') as test_csv:
    test_csv.writelines(
            ['col1,col2,col3\n',
             '1.1,1.2,1.3\n',
             '2.1,2.2,2.3\n'])

# make an npy
os.system('./csv_to_npy test.csv > test.npy')

# open with numpy
test_table = np.load('test.npy')
print test_table
