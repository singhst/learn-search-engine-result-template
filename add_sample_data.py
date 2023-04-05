import pandas as pd

### Crawler
CRAWLER             = pd.read_csv('sample_data/crawler.csv', dtype={"url_id":int, "url":str, "html_content":str})
PARENT_CHILD_LINK   = pd.read_csv('sample_data/parent_child_link.csv', dtype={"url_id":int, "child_url_id":int})
DOC_INFO            = pd.read_csv('sample_data/doc_info.csv', dtype={"url_id":int, "size_of_page":int})
DOC_TOTAL_NUMBER    = pd.read_csv('sample_data/doc_total_number.csv', dtype={"id":int, "n":int})
### Indexer
DOC_TERM_1_GRAM     = pd.read_csv('sample_data/doc_term_1_gram.csv', dtype={"url_id":int, "term_id":int, "term_freq":int})
TERM_1_GRAM         = pd.read_csv('sample_data/term_1_gram.csv', dtype={"term_id":int, "term":str, "doc_freq":int})

SAMPLE_DATASET = {
    ### Crawler
    "crawler": CRAWLER, 
    "parent_child_link": PARENT_CHILD_LINK,
    "doc_info": DOC_INFO,
    "doc_total_number": DOC_TOTAL_NUMBER,
    ### Indexer
    "doc_term_1_gram": DOC_TERM_1_GRAM,
    "term_1_gram": TERM_1_GRAM,
}


if __name__ == "__main__":
    import configparser
    import sqlite3

    ### get config
    full_config_file_path = "./config.ini"
    config = configparser.ConfigParser()
    config.read(full_config_file_path)
    SQLALCHEMY_DATABASE_URI = config["sqlite"].get("connection_str") #"sqlite:///example.db"    #database connection string
    SQLALCHEMY_DATABASE_NAME = config["sqlite"].get("db") #database name

    ### query sample data from DB
    conn=sqlite3.connect(SQLALCHEMY_DATABASE_NAME)
    cur = conn.cursor()
    results = cur.execute("SELECT version_num from alembic_version")
    for row in results:
        print("version_num = ", row[0])

    ### add sample data to DB
    for table_name, records in SAMPLE_DATASET.items():
        records = records.to_dict('records')
        print(records)
        for record in records:
            keys = ', '.join(record.keys())
            values = ', '.join(["?" for _ in range(len(record))])
            query = f"INSERT INTO {table_name} ({keys}) VALUES ({values})"
            print(query)
            print(tuple(record.values()))
            cur.execute(query, tuple(record.values()))
            conn.commit()
    conn.close()