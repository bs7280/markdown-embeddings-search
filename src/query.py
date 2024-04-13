from llama_index.core.indices.vector_store.base import VectorStoreIndex
from llama_index.core.indices.vector_store.retrievers.retriever import (
    VectorIndexRetriever,
)

# from llama_index.retrievers import VectorIndexRetriever
# from llama_index.core.query_engine.reriever_query_engine import RetrieverQueryEngine


# from llama_index

from src.vector_stores import get_postgres_vector_store


def get_index(table_name):
    vector_store = get_postgres_vector_store(table_name=table_name)

    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)
    return index


def get_retriever(table_name):
    index = get_index(table_name=table_name)

    retriever = VectorIndexRetriever(
        index=index,
        similarity_top_k=10,
        # service_context=service_context
    )

    return retriever


def get_query_engine(table_name):

    index = get_index(table_name=table_name)
    query_engine = index.as_query_engine()

    return query_engine
