from llama_index.core import SimpleDirectoryReader, StorageContext
from llama_index.core.indices.vector_store import VectorStoreIndex
from llama_index.vector_stores.postgres import PGVectorStore
import textwrap
import openai
import os
import psycopg2


def get_pinecone_vector_store():
    raise NotImplementedError("TODO suppoert pinecone")


def get_postgres_vector_store(
    table_name,
    embedding_size=1536,
    db_host="localhost",
    db_port="5433",
    db_user="testuser",
    db_password="testpassword",
    db_name="vector_db",
    drop_db=False,
):

    if drop_db:
        conn = psycopg2.connect(
            dbname="postgres",
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
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
        table_name=table_name,
        embed_dim=1536,  # openai embedding dimension
    )

    return vector_store
