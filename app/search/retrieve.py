from typing import List
from app.search.scripts import sentence_transformer_query
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


def result(query: List[str]):
    # query = "SENT_SEARCH: The British government acknowledges that it must take actions beyond addressing its domestic audience."
    
    print(">>> retrieve.py | result() | Retriving pages ...")
    query_results = sentence_transformer_query.process_query(query)
    return query_results


def similar(page_id: str):
    queries = sentence_transformer_query.getTop5_FreqWord(page_id)
    print(">>> retrieve.py | similar() | getTop5_FreqWord() query: `{}`".format(queries))
    
    print(">>> retrieve.py | similar() | Retriving pages ...")
    query_results = sentence_transformer_query.process_query(" ".join(queries)
)
    return query_results, queries
