from fastapi import FastAPI, APIRouter, Query, HTTPException, Request, Depends
from fastapi.templating import Jinja2Templates

from app.db.session import SQLALCHEMY_DATABASE_NAME
import sqlite3

from typing import Optional, Any
from pathlib import Path

from app.recipe_data import RECIPES
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
    conn = sqlite3.connect(SQLALCHEMY_DATABASE_NAME)
    cur = conn.cursor()
    cursor = cur.execute("SELECT version_num from alembic_version")
    for row in cursor:
        print("version_num = ", row[0])
    conn.close()

    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "documents": SAMPLE_DOCUMENTS},
    )


@api_router.get("/search/", status_code=200) ### can ignore schema
def search_keywords(
    *,
    request: Request,
    query: Optional[str] = Query(None, min_length=0, example="chicken"),
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
        {"request": request, "documents": ""},
    )

    ### [x] get "ranked doc" by consine similarity between `input query` and `documents`
    # ranked_doc = getRankedDoc(query)
    ranked_doc = SAMPLE_DOCUMENTS

    ### [ FAKE!!! ]
    # results = filter(lambda recipe: query.lower() in recipe["label"].lower(), RECIPES)
    results = filter(lambda recipe: query.lower() in recipe["title"].lower(), ranked_doc)
    results = list(results)
    results = [{"result_index": i, **doc} for doc, i in zip(results, range(len(results)))]
    print(results)
    return TEMPLATES.TemplateResponse(
        "index.html",
        {"request": request, "documents": results[:max_results]},
    )


@api_router.get("/db/all/", status_code=200)
def get_db_all(
    *,
    max_results: Optional[int] = 10,
) -> dict:
    conn = sqlite3.connect(SQLALCHEMY_DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    query = """
        SELECT *
        FROM crawler
        INNER JOIN parent_child_link
            ON parent_child_link.url_id = crawler.url_id
    """
    records = conn.execute(query).fetchall()
    records = [{k: item[k] for k in item.keys()} for item in records]
    print(records)
    conn.close()
    return {"results": records[:max_results]}


'''@api_router.get("/recipe/{recipe_id}", status_code=200, response_model=Recipe)
def fetch_recipe(*, recipe_id: int) -> Any:
    """
    Fetch a single recipe by ID
    """

    result = [recipe for recipe in RECIPES if recipe["id"] == recipe_id]
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Recipe with ID {recipe_id} not found"
        )

    return result[0]
'''


'''@api_router.get("/search/", status_code=200, response_model=RecipeSearchResults)
def search_recipes(
    *,
    keyword: Optional[str] = Query(None, min_length=3, example="chicken"),
    max_results: Optional[int] = 10,
) -> dict:
    """
    Search for recipes based on label keyword
    """
    if not keyword:
        # we use Python list slicing to limit results
        # based on the max_results query parameter
        return {"results": RECIPES[:max_results]}

    results = filter(lambda recipe: keyword.lower() in recipe["label"].lower(), RECIPES)
    return {"results": list(results)[:max_results]}
'''


'''@api_router.post("/recipe/", status_code=201, response_model=Recipe)
def create_recipe(*, recipe_in: RecipeCreate) -> dict:
    """
    Create a new recipe (in memory only)
    """
    new_entry_id = len(RECIPES) + 1
    recipe_entry = Recipe(
        id=new_entry_id,
        label=recipe_in.label,
        source=recipe_in.source,
        url=recipe_in.url,
    )
    RECIPES.append(recipe_entry.dict())

    return recipe_entry
'''


app.include_router(api_router)


if __name__ == "__main__":
    # Use this for debugging purposes only
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001, log_level="debug")
