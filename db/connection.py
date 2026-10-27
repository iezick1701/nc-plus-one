import os
import psycopg
from dotenv import load_dotenv

load_dotenv()


def get_connection(database=None):
    db_name = database or os.getenv("DB_NAME")
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")

    if not db_name:
        raise RuntimeError("DB_NAME NOT SET")

    connection = psycopg.connect(
        dbname=db_name,
        user=db_user,
        password=db_password,
        host=db_host,
        port=db_port
    )

    return connection