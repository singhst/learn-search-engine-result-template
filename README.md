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
