## Reference link 

https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-7-sqlalchemy-database-setup/

---

## Local Setup for running

1. Current path:
    ```shell
    $ pwd
    /xxxx/learn-search-engine-result-template
    ```
2. `pip install poetry` (or safer, follow the instructions: https://python-poetry.org/docs/#installation)
3. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
4. [UNIX]: Run the FastAPI server via poetry with the bash script: `poetry run ./run.sh`
5. [WINDOWS]: Run the FastAPI server via poetry with the Python command: `poetry run python app/main.py`
6. Open http://localhost:8001/

To stop the server, press CTRL+C

If you get stuck, checkout the [troubleshooting readme](../troubleshooting/README.md)

---

## Full Local Setup

Create tables in DB:
1. Current path:
    ```shell
    $ pwd
    /xxxx/learn-search-engine-result-template
    ```
2. Keep the empty sqlite .db file under root folder ==> `./search_engine.db`
3. Ensure folder `./alembic/versions/` is empty. Delete all files under this folder in the beginning.
4. To create a migration .py (so that the create table SQL can be generated), run below command in terminal:
    ```shell
    $ alembic revision --autogenerate -m "Added initial table"
    ```
5. You will see .py file appears under `./alembic/versions/`
6. To really create tables in SQLite DB, run below command in terminal:
    ```shell
    $ alembic upgrade head
    ```

Add sample data from .csv:
1. Current path:
    ```shell
    $ pwd
    /xxxx/learn-search-engine-result-template
    ```
2. Add,
    ```shell
    $ python add_sample_data.py 
    ```
3. Get data from db,
    ```shell
    $ python app/controller/get_doc_info.py
    ```

Run the API server locally ==> refer to [Local Setup for running](#local-setup-for-running)