## Use a local postgres server
## Guide: https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres.html

import logging
import sys

# Uncomment to see debug logs
logging.basicConfig(stream=sys.stdout, level=logging.ERROR)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from llama_index import SimpleDirectoryReader, StorageContext
from llama_index.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores import PGVectorStore
import textwrap
import openai
import os
import psycopg2

# Pre-req:
# !mkdir -p 'data/paul_graham/'
#!wget 'https://raw.githubusercontent.com/run-llama/llama_index/main/docs/docs/examples/data/paul_graham/paul_graham_essay.txt' -O 'data/paul_graham/paul_graham_essay.txt'

openai.api_key = os.environ["OPENAI_API_KEY"]

connection_string = "postgresql://postgres:password@localhost:5432"
db_host = "localhost"
db_port = "5433"
db_user = "testuser"
db_password = "testpassword"
db_name = "vector_db"

conn = psycopg2.connect(
    dbname="postgres",
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,  # This is the default port for PostgreSQL
)
conn.autocommit = True

try:
    with conn.cursor() as c:
        c.execute(f"DROP DATABASE IF EXISTS {db_name}")
        c.execute(f"CREATE DATABASE {db_name}")
except Exception as e:
    raise e

vector_store = PGVectorStore.from_params(
    database=db_name,
    user=db_user,
    password=db_password,
    host=db_host,
    port=db_port,
    table_name="paul_graham_essay",
    embed_dim=1536,  # openai embedding dimension
)

documents = SimpleDirectoryReader("./data/paul_graham").load_data()
print("Document ID:", documents[0].doc_id)


storage_context = StorageContext.from_defaults(vector_store=vector_store)
index = VectorStoreIndex.from_documents(
    documents, storage_context=storage_context, show_progress=True
)
query_engine = index.as_query_engine()


response = query_engine.query("What did the author do?")

print(textwrap.fill(str(response), 100))

breakpoint()
## https://docs.llamaindex.ai/en/stable/examples/vector_stores/postgres.html
