import os
from pathlib import Path
from typing import Any, List, TYPE_CHECKING

from llama_index.core import (
    VectorStoreIndex,
    get_response_synthesizer,
    download_loader,
    Document,
    StorageContext,
)

if TYPE_CHECKING:
    from langchain.docstore.document import Document as LCDocument

from llama_index.core.readers.base import BaseReader
from llama_index.core.node_parser import SentenceSplitter


from src.vector_stores import get_postgres_vector_store, get_pinecone_vector_store
from src.ingest.document_readers import ObsidianReader


def upload_obsidian_notes(
    vault_dir, storage_type="postgres", table_name="obsidian_vault"
):

    if storage_type == "postgres":
        vector_store = get_postgres_vector_store(table_name=table_name)
    elif storage_type == "":
        vector_store = get_pinecone_vector_store()
        # PineconeVectorStore(pc.Index(index_name))
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    documents = ObsidianReader(vault_dir).load_data()
    parser = SentenceSplitter(chunk_size=2048, chunk_overlap=256 * 2)
    nodes = parser.get_nodes_from_documents(documents)

    # index = VectorStoreIndex.from_documents(
    #    documents
    # )
    # index = VectorStoreIndex(nodes, storage_context=storage_context)
    index = VectorStoreIndex.from_documents(
        documents=documents, storage_context=storage_context, show_progress=True
    )
    query_engine = index.as_query_engine()
    breakpoint()

    return index
