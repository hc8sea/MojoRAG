import sqlite3
from contextlib import contextmanager


@contextmanager
def get_db_connection():
    conn = sqlite3.connect('rag_data.db')
    try:
        yield conn
    finally:
        conn.close()


def create_database():
    with get_db_connection() as conn:
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS RAG_DATA
                     (prompt TEXT, response TEXT, context TEXT)''')
        conn.commit()


create_database()


def insert_data_into_db(prompt, response, context):

    conn = sqlite3.connect('rag_data.db')
    c = conn.cursor()
    c.execute("INSERT INTO RAG_DATA (prompt, response, context) VALUES (?, ?, ?)",
              (prompt, response, context))

    conn.commit()
    conn.close()
