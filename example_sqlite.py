from typing import Type, List, Union
import sqlite3
from sqlite3 import Connection


def create_table(connection: Type[Connection]):
    # Schema defining the table holding our data
    SCHEMA = """
        CREATE TABLE IF NOT EXISTS example_table (
            fpath TEXT, 
            n_measure INTEGER, 
            treatment TEXT, 
            amplitude REAL
        )"""
    # Create the table, commit it, and close the connection
    connection.execute(SCHEMA)
    connection.commit()


def drop_table(connection: Type[Connection]):
    query = """
        DROP TABLE IF EXISTS example_table;
    """
    # Create the table, commit it, and close the connection
    connection.execute(query)
    connection.commit()


def insert_data(connection: Type[Connection]):
    test_data = [
        {
            "fpath": "path/to/file/one.dat",
            "n_measure": 1,
            "treatment": "Control",
            "amplitude": 50.5,
        },
        {
            "fpath": "path/to/file/two.dat",
            "n_measure": 2,
            "treatment": "Control",
            "amplitude": 76.5,
        },
        {
            "fpath": "path/to/file/three.dat",
            "n_measure": 1,
            "treatment": "Experimental",
            "amplitude": 5.5,
        },
    ]
    for item in test_data:
        connection.execute(
            "INSERT INTO example_table (fpath, n_measure, treatment, amplitude) VALUES(:fpath, :n_measure, :treatment, :amplitude)",
            item,
        )
        connection.commit()  # commit after each addition
        print(f"Added data {item['fpath']}") # print a helpful message once added


def select_as_list_of_dict(connection: Type[Connection]) -> List[dict]:
    ### query data as `list of dict` from DB
    connection.row_factory = sqlite3.Row
    query = """
        SELECT * FROM example_table WHERE treatment = 'Experimental'
    """
    records = connection.execute(query).fetchall()
    records = [{k: item[k] for k in item.keys()} for item in records]
    print(records)
    return records


if __name__ == "__main__":
    ### setup for sqlite
    SQLALCHEMY_DATABASE_NAME = 'search_engine.db'
    conn = sqlite3.connect(SQLALCHEMY_DATABASE_NAME)
    cur = conn.cursor()

    drop_table(connection=conn)

    create_table(connection=conn)

    insert_data(connection=conn)

    ### query data as `list of dict` from DB
    select_as_list_of_dict(conn)

    conn.close()
