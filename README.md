# Local Setup for running

## (1) Crawler and Indexer

To run in Linux:
```shell
$ pwd
/xxxx/learn-search-engine-result-template

$ pip install -r requirements.txt

### Normal version
$ python crawler_and_index_sqlitedict.py
$ python indexer-tfidf_v1.py
```


## (2) Search Engine - Web interface
1. Current path:
    ```shell
    $ pwd
    /xxxx/learn-search-engine-result-template
    
    $ ls
    README.md               app                     pyproject.toml          run.sh                  stopwords.txt
    alembic.ini             poetry.lock             requirements.txt        sample_data             venv
    ```
2. `pip install poetry==1.4.2` (or safer, follow the instructions: https://python-poetry.org/docs/#installation)
3. Install dependencies `cd` into the directory where the `pyproject.toml` is located then `poetry install`
4. [UNIX]: Run the FastAPI server via poetry with the bash script: `poetry run ./run.sh`
5. [WINDOWS]: Run the FastAPI server via poetry with the Python command: `poetry run run.sh`
6. Open http://localhost:8001/

To stop the server, press CTRL+C


## (3) Crawler and Indexer (Sentence Transformer version)

> ---
> 
> *NOT SUPPORT `GET SIMILAR PAGES` FEATURE*
>
> ---

To run in Linux:
```shell
$ pwd
/xxxx/learn-search-engine-result-template

$ pip install -r requirements.txt

### Sentence Transformer version
$ python sentence_transformer_crawler.py
$ python sentence_transformer_indexer.py
```

Then go back to `(2) Search Engine - Web interface`, but must enter URL: `http://localhost:8001/search/sentence-transformer?query=xxxx` in browser to use the Sentence Transformer searching feature.


# Demo Video

https://www.youtube.com/watch?v=ZTa8D6w3hbg

https://user-images.githubusercontent.com/71545537/234554295-e2409013-5377-4894-bd97-d1557fc85ec0.mp4
