from typing import List
from app.search.scripts import utils, similarity_query
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


def result(query: List[str]):
    # Split double quotes phrases
    queries = utils.splitQuery(query)
    # Clean, stem ...
    queries = utils.clean(queries)
    print(">>> view.py | result() | Processed query: `{}`".format(queries))
    
    print(">>> view.py | result() | Retriving pages ...")
    query_results = similarity_query.retrive_func(queries)
    return query_results


def similar(page_id: str):
    queries = similarity_query.getTop5_FreqWord(page_id)
    print(">>> view.py | similar() | getTop5_FreqWord() query: `{}`".format(queries))
    
    print(">>> view.py | similar() | Retriving pages ...")
    query_results = similarity_query.retrive_func(queries)
    return query_results, queries