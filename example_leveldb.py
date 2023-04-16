"""
https://zhuanlan.zhihu.com/p/32229953
"""

#!/usr/bin/env python
#-*-coding: utf-8-*-

import leveldb
import os, sys
from typing import List

db_path = "./sample_leveldb_database"

def initialize():
    db = leveldb.LevelDB(db_path)
    return db

def insert(db, sid, name):
    db.Put(str(sid).encode(), name.encode())

def delete(db, sid):
    db.Delete(str(sid).encode())

def update(db, sid, name):
    db.Put(str(sid).encode(), name.encode())

def search(db, sid):
    name = db.Get(str(sid).encode())
    return name

def return_all(db) -> List[tuple]:
    return list(db.RangeIter())

### `batch_read()` not work
def batch_read(db, sid_list: List[str]) -> List[tuple]:
    batch = db.WriteBatch()
    for sid in sid_list:
        batch.get(sid.encode())
    for key, value in db.RangeIter(batch):
        print('Key:', key, 'Value:', value)


if __name__ == "__main__":
    db = initialize()

    print("Insert 3 records.")
    print(str(1).encode())
    insert(db, 1, "Alice")
    insert(db, 2, "Bob")
    insert(db, 2, "xxxxx")
    insert(db, 2, "yyyy")
    insert(db, 3, "Peter")
    insert(db, "term1", "keyword1")
    print(return_all(db))

    print("Delete the record where sid = 1.")
    delete(db, 1)
    print(return_all(db))

    print("Update the record where sid = 3.")
    update(db, 3, "Mark")
    print(return_all(db))

    print("Get the name of student whose sid = 2.")
    name = search(db, 2)
    print(name)

    print("Get the name of student whose sid = 3.")
    name = search(db, 3)
    print(name)

    print("Get the name of student whose sid = 'term1'.")
    name = search(db, "term1")
    print(name)

    print(return_all(db))

    batch_read(db, ['3','1'])

    # os.system(f"rm -r {db_path}")

### Output
# (venv) Sing:learn-search-engine-result-template Sing$ venv/bin/python example_leveldb.py 
# Insert 3 records.
# b'1'
# [(bytearray(b'1'), bytearray(b'Alice')), (bytearray(b'2'), bytearray(b'yyyy')), (bytearray(b'3'), bytearray(b'Peter'))]
# Delete the record where sid = 1.
# [(bytearray(b'2'), bytearray(b'yyyy')), (bytearray(b'3'), bytearray(b'Peter'))]
# Update the record where sid = 3.
# [(bytearray(b'2'), bytearray(b'yyyy')), (bytearray(b'3'), bytearray(b'Mark'))]
# Get the name of student whose sid = 2.
# bytearray(b'yyyy')
# Get the name of student whose sid = 3.
# bytearray(b'Mark')
# [(bytearray(b'2'), bytearray(b'yyyy')), (bytearray(b'3'), bytearray(b'Mark'))]
# Traceback (most recent call last):
#   File "example_leveldb.py", line 73, in <module>
#     batch_read(db, ['3','1'])
#   File "example_leveldb.py", line 36, in batch_read
#     batch = db.WriteBatch()
# AttributeError: 'leveldb.LevelDB' object has no attribute 'WriteBatch'