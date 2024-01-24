from pathlib import Path
import os
from llama_index import (
    VectorStoreIndex,
    get_response_synthesizer,
    download_loader,
    Document
)
from llama_index.retrievers import VectorIndexRetriever
from llama_index.schema import MetadataMode
from llama_index.postprocessor import SimilarityPostprocessor
from llama_index.query_engine import RetrieverQueryEngine

## Load from local markdown files
MarkdownReader = download_loader("MarkdownReader")
loader = MarkdownReader()

all_documents = []
for fname in ['./test_data/doc_01.md']:
    documents = loader.load_data(file=Path('./test_data/doc_01.md'))

    # Add arbitrary meta data
    for doc in documents:
        doc.metadata = {
            'file_name': os.path.split(fname)[1],
            'category': 'documentation',
            'author': 'bob'
        }
        #doc.excluded_llm_metadata_keys=["file_name"],

        all_documents.append(doc)

## Adding a custom document

document = Document(
    text="This is a super-customized document",
    metadata={
        "file_name": "super_secret_document.txt",
        "category": "finance",
        "author": "LlamaIndex",
    },
    excluded_llm_metadata_keys=["file_name"],
    metadata_seperator="::",
    metadata_template="{key}=>{value}",
    text_template="Metadata: {metadata_str}\n-----\nContent: {content}",
)

print(
    "The LLM sees this: \n",
    document.get_content(metadata_mode=MetadataMode.LLM),
)
print(
    "The Embedding model sees this: \n",
    document.get_content(metadata_mode=MetadataMode.EMBED),
)

## add custom document to all documents
all_documents.append(document)

## Use OpenAI for index
vector_index = VectorStoreIndex.from_documents(all_documents)

## Or more complex retriever
retriever = VectorIndexRetriever(
    index=vector_index,
    similarity_top_k=10,
)

# configure response synthesizer
response_synthesizer = get_response_synthesizer()

# assemble query engine
query_engine = RetrieverQueryEngine(
    retriever=retriever,
    #response_synthesizer=response_synthesizer,
    #node_postprocessors=[SimilarityPostprocessor(similarity_cutoff=0.7)],
)

# query
response = query_engine.query("What is the customized document")
breakpoint()

## Use locally
# Note - Uses llama-cpp
# `pip install llama-cpp-python`
if False:
    from llama_index import ServiceContext
    service_context = ServiceContext.from_defaults(
        #embed_model="local:BAAI/bge-large-en", 
        llm="local:BAAI/bge-large-en",
        embed_model="local"
    )

    breakpoint()