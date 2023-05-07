from typing import List
from app.search.scripts import similarity_query, sentence_transformer_query
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


def result(query: List[str]):
    # query = "SENT_SEARCH: The British government acknowledges that it must take actions beyond addressing its domestic audience."
    
    print(">>> retrieve.py | result() | Retriving pages ...")
    query_results = sentence_transformer_query.process_query(query)
    return query_results


# def result(query: List[str]):
#     # Split double quotes phrases
#     queries = similarity_query.split_query_quot(query)
#     # Clean, stem ...
#     queries = similarity_query.clean_stem_query(queries)
#     print(">>> retrieve.py | result() | Processed query: `{}`".format(queries))
    
#     print(">>> retrieve.py | result() | Retriving pages ...")
#     query_results = similarity_query.retrive_func(queries)
#     return query_results


def similar(page_id: str):
    queries = similarity_query.getTop5_FreqWord(page_id)
    print(">>> retrieve.py | similar() | getTop5_FreqWord() query: `{}`".format(queries))
    
    print(">>> retrieve.py | similar() | Retriving pages ...")
    query_results = similarity_query.retrive_func(queries)
    return query_results, queries