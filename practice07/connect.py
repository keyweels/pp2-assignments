import psycopg2
from config import get_config


def test_connection():
    config = get_config()
    conn = psycopg2.connect(**config)
    print("Connected successfully")
    conn.close()


test_connection()