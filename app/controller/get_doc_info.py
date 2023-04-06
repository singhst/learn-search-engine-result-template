from typing import Type, List, Union
import sqlite3
from sqlite3 import Connection


def get_data_by_query(connection: Type[Connection], query: str) -> List[dict]:
    records = connection.execute(query).fetchall()
    records = [{k: item[k] for k in item.keys()} for item in records]
    return records


def get_doc_info_by_id(connection: Type[Connection], doc_id_list: List[Union[str,int]]) -> List[dict]:
    connection.row_factory = sqlite3.Row
    doc_id_list = ','.join([str(_) for _ in doc_id_list])
    query = """
        SELECT
            doc_info.url_id
            , doc_info.title
            , doc_info.url
            , doc_info.last_modification_date
            , doc_info.size_of_page
        FROM doc_info
        WHERE
            1=1
            AND doc_info.url_id in ({doc_id_list})
        ORDER BY 
            doc_info.url_id
    """.format(doc_id_list=doc_id_list)
    return get_data_by_query(connection=connection, query=query)


def get_top_keywords_by_a_id(connection: Type[Connection], doc_id: Union[str,int], max_keyword_num: int = 5) -> List[dict]:
    ### query data as `list of dict` from DB
    connection.row_factory = sqlite3.Row
    query = """
        SELECT
            doc_term_1_gram.url_id
            , doc_term_1_gram.term_id
            , doc_term_1_gram.term_freq
            , term_1_gram.term
        FROM doc_term_1_gram
        LEFT JOIN term_1_gram
            ON term_1_gram.term_id = doc_term_1_gram.term_id
        WHERE
            1=1
            AND doc_term_1_gram.url_id in ({doc_id})
        ORDER BY 
            doc_term_1_gram.url_id
        LIMIT {max_keyword_num}
    """.format(doc_id=doc_id, max_keyword_num=max_keyword_num)
    return get_data_by_query(connection=connection, query=query)


def get_parent_child_links_by_a_id(connection: Type[Connection], doc_id: Union[str,int], parent_or_child: str = 'parent') -> List[dict]:
    ### query data as `list of dict` from DB
    connection.row_factory = sqlite3.Row
    column_names = {
        "parent": "url_id",
        "child": "child_url_id",
    }
    inverse_column_names = {k: v for k in column_names for v in column_names.values() if column_names[k] != v}
    # print(">>> get_parent_child_links_by_a_id() | inverse_column_names:", inverse_column_names)
    query = """
        SELECT
            DISTINCT
            parent_child_link.{column_name}
            , doc_info.url
        FROM parent_child_link
        LEFT JOIN doc_info
            ON doc_info.url_id = parent_child_link.{column_name}
        WHERE
            1=1
            AND parent_child_link.{column_name_inverse} in ({doc_id})
        ORDER BY 
            parent_child_link.{column_name}
    """.format(column_name=column_names[parent_or_child],
               column_name_inverse=inverse_column_names[parent_or_child],
               doc_id=doc_id
               )
    return get_data_by_query(connection=connection, query=query)



if __name__ == "__main__":
    ### setup for sqlite
    SQLALCHEMY_DATABASE_NAME = 'search_engine.db'
    conn = sqlite3.connect(SQLALCHEMY_DATABASE_NAME)
    cur = conn.cursor()

    ## Examples
    doc_id_list = [1,2,3]
    doc_info_list = get_doc_info_by_id(conn, doc_id_list=doc_id_list)
    print("(1) get_doc_info_by_id\n", doc_info_list)

    results = []
    for doc_info in doc_info_list:
        doc_id = doc_info.get('url_id')
        doc_info['keywords'] = get_top_keywords_by_a_id(conn, doc_id=doc_id)
        doc_info['parent_links'] = get_parent_child_links_by_a_id(conn, doc_id=doc_id, parent_or_child='parent')
        doc_info['child_links'] = get_parent_child_links_by_a_id(conn, doc_id=doc_id, parent_or_child='child')
        results.append(doc_info)

    print("results:", results)
    conn.close()
