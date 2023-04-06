import configparser
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

full_config_file_path = "./config.ini"
config = configparser.ConfigParser()
config.read(full_config_file_path)

SQLALCHEMY_DATABASE_URI = config["sqlite"].get("connection_str") #"sqlite:///example.db"    #database connection string
SQLALCHEMY_DATABASE_NAME = config["sqlite"].get("db") #database name

# [For SQLite connection]
engine = create_engine(
    SQLALCHEMY_DATABASE_URI,
    # echo=False, # stop printing SQL statement when doing CRUD operations
    echo=True,
    # only required for sqlite
    connect_args={"check_same_thread": False},
)

'''
DB connection string format:
    dialect[+driver]://user:password@host/dbname[?key=value..]
dialect:    mysql, oracle, postgresql, etc.
driver:     the name of a DBAPI, such as psycopg2, pyodbc, cx_oracle, etc.
'''
# # [For postgresql connection]
# engine = create_engine("postgresql://scott:tiger@localhost/test")

# # [For docker container postgresql]
# engine = create_engine("postgresql://scott:tiger@hostname/dbname",
#                             encoding='latin1', echo=True)

# # [For mysql connection]
# engine = create_engine("mysql://scott:tiger@hostname/dbname",
#                             encoding='latin1', echo=True)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
