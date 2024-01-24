
import os
from pathlib import Path
from typing import Any, List, TYPE_CHECKING

from llama_index import (
    VectorStoreIndex,
    get_response_synthesizer,
    download_loader,
    Document,
    StorageContext,
)
from pinecone import Pinecone, ServerlessSpec
from llama_index.vector_stores import PineconeVectorStore

if TYPE_CHECKING:
    from langchain.docstore.document import Document as LCDocument

from llama_index.readers.base import BaseReader
from llama_index.readers.file.markdown_reader import MarkdownReader
from llama_index.readers.file.flat_reader import FlatReader
from llama_index.readers.schema.base import Document
from llama_index.retrievers import VectorIndexRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.postprocessor import SimilarityPostprocessor
from llama_index.node_parser import SentenceSplitter

import os

## params

notes_dir = '/Users/benshaughnessy/Documents/personalvault-1'
index_name = "mynotes-2"

## #####

## Modified built in version
class ObsidianReader(BaseReader):
    """Utilities for loading data from an Obsidian Vault.

    Args:
        input_dir (str): Path to the vault.

    """

    def __init__(self, input_dir: str):
        """Init params."""
        self.input_dir = Path(input_dir)

    def load_data(self, *args: Any, **load_kwargs: Any) -> List[Document]:
        """Load data from the input directory."""
        docs: List[Document] = []
        for dirpath, dirnames, filenames in os.walk(self.input_dir):
            dirnames[:] = [d for d in dirnames if not d.startswith(".")]
            for filename in filenames:
                if filename.endswith(".md"):
                    filepath = os.path.join(dirpath, filename)

                    if load_kwargs.get('reader') == 'markdown':
                        content = MarkdownReader().load_data(Path(filepath))

                        for doc in content:
                            doc.metadata = {
                                "file_name": filename,
                            }
                    else:
                        content = FlatReader().load_data(Path(filepath))


                    docs.extend(content)
        return docs

    def load_langchain_documents(self, **load_kwargs: Any) -> List["LCDocument"]:
        """Load data in LangChain document format."""
        docs = self.load_data(**load_kwargs)
        return [d.to_langchain_format() for d in docs]


# init pinecone
pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

write_data=False
if write_data:
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            index_name,
            dimension=1536,
            metric="euclidean",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-west-2'
            )  
        )

    # construct vector store and customize storage context
    storage_context = StorageContext.from_defaults(
        vector_store=PineconeVectorStore(pc.Index(index_name))
    )

    documents = ObsidianReader(notes_dir).load_data()
    parser = SentenceSplitter(
        chunk_size=2048,
        chunk_overlap=256*2
    )
    nodes = parser.get_nodes_from_documents(documents)

    #index = VectorStoreIndex.from_documents(
    #    documents
    #)
    index = VectorStoreIndex(nodes, storage_context=storage_context)
    #index = VectorStoreIndex.from_documents(
    #    documents, storage_context=storage_context
    #)
else:
    vector_store = PineconeVectorStore(pc.Index(index_name))
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)



# configure retriever
retriever = VectorIndexRetriever(
    index=index,
    similarity_top_k=10,
)

# configure response synthesizer
response_synthesizer = get_response_synthesizer()


# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    response_synthesizer=response_synthesizer,
    #node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)

#query_engine = index.as_query_engine()
def ask(query, query_engine=query_engine):
    return query_engine.query(query)

def list_files(query, retriever=retriever, k=10):
    [
        print(f"{doc.metadata.get('filename')}:\n--------------\n{doc.text}\n------\n") 
        for doc in retriever.retrieve(query)[:k]
    ]

query = "What ideas have I written down relating to the macos workflow tool Alfred?"
response = ask(query)

print(response.response)

list_files(query, k=2)
