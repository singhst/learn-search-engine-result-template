from fastapi import FastAPI, APIRouter, Query, Request
from fastapi.templating import Jinja2Templates

from app.search import retrieve

from typing import Optional
from pathlib import Path

from app.document_sample_data import SAMPLE_DOCUMENTS


BASE_PATH = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_PATH / "templates"))


app = FastAPI(title="Search Engine", openapi_url="/openapi.json")

api_router = APIRouter()


# Updated to serve a Jinja2 template
# https://www.starlette.io/templates/
# https://jinja.palletsprojects.com/en/3.0.x/templates/#synopsis
'''@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "recipes": RECIPES},
    )'''
@api_router.get("/", status_code=200)
def root(request: Request) -> dict:
    """
    Root GET
    """
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            # "documents": SAMPLE_DOCUMENTS
        },
    )


@api_router.get("/search", status_code=200)
def search_keywords(
    *,
    request: Request,
    query: Optional[str] = Query(None, min_length=0, example=["comput", "scienc"]),
    max_results: Optional[int] = 50,
) -> dict:
    """
    Search for documents based on keywords in query
    """
    if not query:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return TEMPLATES.TemplateResponse(
            "index.html",
            {"request": request, "documents_num": 0, "documents": ""},
        )
    
    print(">>> main.py | search_keywords() | Origin query: {}".format(query))
    
    ### get "ranked doc" by cosine similarity between `input query` and `documents`
    query_results = retrieve.result(query)
    print(">>> main.py | search_keywords() | str(query_results)[:200]: {}".format(str(query_results)[:200]))
    
    query_results = query_results[:max_results]
    documents_num = len(query_results)
    print(">>> main.py | search_keywords() | len(query_results): {}".format(len(query_results)))
    
    query_results = [{"result_index": i+1, **doc} for doc, i in zip(query_results, range(len(query_results)))]
    # return query_results
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "query": query,
            "documents_num": documents_num,
            "documents": query_results
        },
    )


@api_router.get("/search/test", status_code=200)
def search_keywords_test(
    *,
    request: Request,
    query: Optional[str] = Query(None, min_length=0, example=["comput", "scienc"]),
    max_results: Optional[int] = 50,
) -> dict:
    """
    Search for documents based on keywords in query
    """
    if not query:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return TEMPLATES.TemplateResponse(
            "index.html",
            {"request": request, "documents_num": 0, "documents": ""},
        )
    
    ranked_doc = SAMPLE_DOCUMENTS
    
    ### [ FAKE!!! ]
    results = filter(lambda recipe: query.lower() in recipe["title"].lower(), ranked_doc)
    results = list(results)
    results = [{"result_index": i, **doc} for doc, i in zip(results, range(len(results)))]
    print(results)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request, 
            "documents": results[:max_results]
        },
    )


@api_router.get("/search/similar", status_code=200)
def get_similar_pages(
    *,
    request: Request,
    page_id: Optional[str] = Query(None, min_length=0, example=["comput", "scienc"]),
    max_results: Optional[int] = 50,
) -> dict:
    """
    Search for documents based on top 5 most frequent keywords which are from one of the previous returned pages
    """
    if not page_id:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return TEMPLATES.TemplateResponse(
            "index.html",
            {"request": request, "documents_num": 0, "documents": ""},
        )
    print(">>> main.py | get_similar_pages() | Origin query: {}".format(page_id))
    
    ### get "ranked doc" by cosine similarity between `input query` and `documents`
    query_results, top5_keywords = retrieve.similar(page_id)
    print(">>> main.py | get_similar_pages() | str(query_results)[:200]: {}".format(str(query_results)[:200]))
    
    query_results = query_results[:max_results]
    documents_num = len(query_results)
    print(">>> main.py | get_similar_pages() | len(query_results): {}".format(len(query_results)))
    
    query_results = [{"result_index": i+1, **doc} for doc, i in zip(query_results, range(len(query_results)))]
    # return query_results
    return TEMPLATES.TemplateResponse(
        "index.html",
        {
            "request": request,
            "page_id": page_id,
            "query": top5_keywords,
            "documents_num": documents_num,
            "documents": query_results
        },
    )


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn
    
    uvicorn.run(app, host="localhost", port=8001, log_level="debug")
