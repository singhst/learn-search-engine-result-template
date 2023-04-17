from typing import List
from app.search.scripts import utils, similarity_query
from pathlib import Path

BASE_PATH = Path(__file__).resolve().parent


query_results = [
    ["1", "title1", "urlname1", 0, "lastmod1", "size1", [("key1", 1), ("key2", 2)], ["p1", "p2"], ["c1", "c2"]],
    ["2", "title2", "urlname2", 1, "lastmod2", "size2", [("key1", 1), ("key2", 2)], ["p1", "p2"], ["c1", "c2"]],
    ]


def result(query: List[str]):
    # Split double quotes phrases
    queries = utils.splitQuery(query)
    # Clean, stem ...
    queries = utils.clean(queries)
    print(">>> view.py | result() | Processed query: `{}`".format(queries))
    
    print(">>> view.py | result() | Retriving pages ...")
    query_results = similarity_query.retrive_func(queries)
    return query_results


# def similar(request):
#     if request.method == 'GET':
#         form = ReQueryForm(request.GET)
#         if form.is_valid():
#             doc_id = form.cleaned_data['docId']
#             queries = retrivedb.getFreqWordAsQueryList(doc_id)
#             print(queries)

#             query_results = retrivedb.retrive(queries)
#             """Peter's retrive function"""
#             # peter_results = cosineSimilarity.runQuery(queries)
#             # query_results = retrivedb.reformatPeterResult(peter_results)
#             return render(request, 'search/result.html', {'query_results': query_results})
#         else:
#             return render(request, 'search/index.html')
