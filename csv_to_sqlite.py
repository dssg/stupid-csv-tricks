#!/usr/bin/env python

import sqlite3
import argparse
import os
from datetime import datetime
import itertools as it

import numpy as np

from diogenes.read import open_csv
from diogenes.utils import NOT_A_TIME

def __sqlite_type(np_descr):
    if 'b' in np_descr:
        return 'BOOLEAN'
    if 'i' in np_descr:
        return 'INTEGER'
    if 'f' in np_descr:
        return 'REAL'
    if 'S' in np_descr:
        return 'TEXT'
    if 'M' in np_descr or 'm' in np_descr:
        return 'INTEGER'
    raise ValueError('No sqlite type found for np type: {}'.format(np_descr))

EPOCH = datetime.utcfromtimestamp(0)
def np_time_to_unix_time(dt):
    # from 
    # http://stackoverflow.com/questions/6999726/how-can-i-convert-a-datetime-object-to-milliseconds-since-epoch-unix-time-in-p
    # and
    # http://stackoverflow.com/questions/29753060/how-to-convert-numpy-datetime64-into-datetime
    return (dt.astype('O') - EPOCH).total_seconds()

def __make_digestible_list_of_list(sa):
    res_cols = []
    for col_name, dtype in sa.dtype.descr:
        col = sa[col_name]
        if 'i' in dtype:
            res_cols.append([None if cell == -999 else cell for cell in
                             col])
        elif 'f' in dtype:
            res_cols.append([None if np.isnan(cell) else cell for cell in
                             col])
        elif 'm' in dtype or 'M' in dtype:
            res_cols.append([None if cell == NOT_A_TIME else 
                             np_time_to_unix_time(cell) for cell in col])
        else:
            res_cols.append(col)
    return it.izip(*res_cols)

def csv_to_sqlite(csv_path, sqlite_path=None, table_name=None):
    if sqlite_path is None:
        sqlite_path = os.path.splitext(csv_path)[0] + '.db'
    if table_name is None:
        table_name = os.path.splitext(os.path.basename(csv_path))[0]
    conn = sqlite3.connect(sqlite_path)
    sql_drop = 'DROP TABLE IF exists "{}"'.format(table_name)
    conn.execute(sql_drop)
    sa = open_csv(csv_path)
    col_names = sa.dtype.names
    sqlite_types = [__sqlite_type(np_descr) for _, np_descr in sa.dtype.descr]
    sql_create = 'CREATE TABLE "{}" ({})'.format(
            table_name,
            ', '.join(['{} {}'.format(col_name, sqlite_type) for 
                       col_name, sqlite_type 
                       in zip(col_names, sqlite_types)]))
    conn.execute(sql_create)
    data = __make_digestible_list_of_list(sa)
    sql_insert = 'INSERT INTO "{}" VALUES ({})'.format(
            table_name,
            ', '.join('?' * len(col_names)))
    conn.executemany(sql_insert, data)
    conn.commit()
    conn.close()
    return (sqlite_path, table_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
            description='Converts a csv to an sqlite db')
    parser.add_argument('--sqlite_path', '-o', default=None,
                        help='Sqlite database file to be created')
    parser.add_argument('--table_name', '-t', default=None,
                        help='Name of table in sqlite database')
    parser.add_argument('csv_path', help='Name of CSV file to convert')
    args = parser.parse_args()
    sqlite_path, table_name = csv_to_sqlite(
            args.csv_path, 
            sqlite_path=args.sqlite_path,
            table_name=args.table_name)
    print 'written to file: {}, table: "{}"'.format(sqlite_path, table_name)
