## Use a local postgres server
## Guide: https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres.html

from llama_index import SimpleDirectoryReader, StorageContext
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
import textwrap
import openai

import psycopg2

connection_string = "postgresql://postgres:password@localhost:5432"
db_name = "vector_db"
conn = psycopg2.connect(connection_string)
conn.autocommit = True

with conn.cursor() as c:
    c.execute(f"DROP DATABASE IF EXISTS {db_name}")
    c.execute(f"CREATE DATABASE {db_name}")

breakpoint()
## https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres.html
