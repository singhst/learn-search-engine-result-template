"""
https://zhuanlan.zhihu.com/p/32229953
"""

#!/usr/bin/env python
#-*-coding: utf-8-*-

import leveldb
import os, sys

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

def display(db):
    for key, value in db.RangeIter():
        print (key, value)

def return_all(db):
    return list(db.RangeIter())


if __name__ == "__main__":
    db = initialize()

    print("Insert 3 records.")
    print(str(1).encode())
    insert(db, 1, "Alice")
    insert(db, 2, "Bob")
    insert(db, 3, "Peter")
    display(db)

    print("Delete the record where sid = 1.")
    delete(db, 1)
    display(db)

    print("Update the record where sid = 3.")
    update(db, 3, "Mark")
    display(db)

    print("Get the name of student whose sid = 3.")
    name = search(db, 3)
    print(name)

    print(return_all(db))

    # os.system(f"rm -r {db_path}")

### Output
# (venv) Sing:learn-search-engine-result-template Sing$ venv/bin/python test_leveldb.py 
# Insert 3 records.
# b'1'
# bytearray(b'1') bytearray(b'Alice')
# bytearray(b'2') bytearray(b'Bob')
# bytearray(b'3') bytearray(b'Peter')
# Delete the record where sid = 1.
# bytearray(b'2') bytearray(b'Bob')
# bytearray(b'3') bytearray(b'Peter')
# Update the record where sid = 3.
# bytearray(b'2') bytearray(b'Bob')
# bytearray(b'3') bytearray(b'Mark')
# Get the name of student whose sid = 3.
# bytearray(b'Mark')
# [(bytearray(b'2'), bytearray(b'Bob')), (bytearray(b'3'), bytearray(b'Mark'))]