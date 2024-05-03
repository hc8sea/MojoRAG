from dotenv import load_dotenv, find_dotenv
import sys

# Workaround to force ChromaDB compatibility with older versions of Python
__import__('pysqlite3')
sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')

_ = load_dotenv(find_dotenv())
