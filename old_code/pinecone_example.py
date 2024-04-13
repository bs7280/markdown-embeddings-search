from pinecone import Pinecone, ServerlessSpec
from llama_index import VectorStoreIndex, SimpleDirectoryReader, StorageContext
from llama_index.vector_stores import PineconeVectorStore
import os

# init pinecone
pc = Pinecone(
    api_key=os.environ.get("PINECONE_API_KEY")
)

write_data=False
if write_data:
    #pc.init(api_key="")#, environment="<environment>")
    if "quickstart" not in pc.list_indexes().names():
        pc.create_index(
            "quickstart",
            dimension=1536,
            metric="euclidean",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-west-2'
            )  
        )

    # construct vector store and customize storage context
    storage_context = StorageContext.from_defaults(
        vector_store=PineconeVectorStore(pc.Index("quickstart"))
    )

    # Load documents and build index
    documents = SimpleDirectoryReader(
        "data/paul_graham"
    ).load_data()
    index = VectorStoreIndex.from_documents(
        documents, storage_context=storage_context
    )
else:
    vector_store = PineconeVectorStore(pc.Index("quickstart"))
    index = VectorStoreIndex.from_vector_store(vector_store=vector_store)

q = index.as_query_engine()

def ask(query, query_engine=q):
    return query_engine.query(query)
breakpoint()