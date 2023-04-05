## Reference link 

https://christophergs.com/tutorials/ultimate-fastapi-tutorial-pt-7-sqlalchemy-database-setup/

## Local Setup

1. `pip install poetry` (or safer, follow the instructions: https://python-poetry.org/docs/#installation)
2. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
3. [UNIX]: Run the FastAPI server via poetry with the bash script: `poetry run ./run.sh`
4. [WINDOWS]: Run the FastAPI server via poetry with the Python command: `poetry run python app/main.py`
5. Open http://localhost:8001/

To stop the server, press CTRL+C

If you get stuck, checkout the [troubleshooting readme](../troubleshooting/README.md)

---
## Deal with SQLite DB

1. Keep the empty sqlite .db file under root folder ==> `./search_engine.db`
2. Ensure folder `./alembic/versions/` is empty. Delete all files under this folder in the beginning.
3. To create a migration .py (so that the create table SQL can be generated), run below command in terminal:
    ```shell
    $ alembic revision --autogenerate -m "Added initial table"
    ```
4. You will see .py file appears under `./alembic/versions/`
5. To really create tables in SQLite DB, run below command in terminal:
    ```shell
    $ alembic upgrade head
    ```