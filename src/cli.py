import argparse
from src.uploader import upload_obsidian_notes
from src.vector_stores import get_postgres_vector_store
from src.query import get_query_engine, get_retriever

import logging
import sys

logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def get_argparser():
    # create the parser
    parser = argparse.ArgumentParser(description="Process some data")

    # create subparsers
    subparsers = parser.add_subparsers(dest="command")

    # create the parser for the 'query' command
    query_parser = subparsers.add_parser("query", help="Prompt RAG model with query")
    query_parser.add_argument(
        "--query", "-q", type=str, help="Specify the prompt query"
    )

    # create the parser for the 'upload' command
    upload_parser = subparsers.add_parser("upload", help="Upload notes to vector store")
    upload_parser.add_argument(
        "--source-type",
        "-s",
        choices=["notes", "imessage"],
        default="notes",
        help="Specify the source type (default: notes)",
    )
    upload_parser.add_argument(
        "--destination",
        "-d",
        choices=["postgres", "pinecone"],
        default="postgres",
        help="Specify the source type (default: postgres)",
    )

    search_parser = subparsers.add_parser(
        "search", help="Search notes with query and return top 10 results"
    )
    search_parser.add_argument(
        "--query", "-q", type=str, help="Specify the search query"
    )

    help_parser = subparsers.add_parser(
        "help", help="Show help message for all available commands"
    )

    return parser


####

vault_dir = "/Users/benshaughnessy/Documents/personalvault-1"

parser = get_argparser()
args = parser.parse_args()


# do something based on the command
if args.command == "query":
    print("Performing query operation...")

    query_engine = get_query_engine("obsidian_vault")

    # query_engine = index.as_query_engine()
    def ask(query, query_engine=query_engine):
        return query_engine.query(query)

    query = "What ideas have I written down relating to the macos workflow tool Alfred?"

    print(ask(args.query))
elif args.command == "search":
    retriever = get_retriever("obsidian_vault")

    def list_files(query, retriever=retriever, k=10):
        [
            print(
                f"{doc.metadata.get('filename')}:"  # \n--------------\n{doc.text}\n------\n"
            )
            for doc in retriever.retrieve(query)[:k]
        ]

    list_files(args.query)

elif args.command == "upload":
    print(f"Performing upload operation with source type: {args.source_type}")
    if args.source_type == "notes":
        upload_obsidian_notes(
            vault_dir, storage_type="postgres", table_name="obsidian_vault"
        )
    else:
        raise NotImplementedError("Error")
elif args.command == "help":
    parser.print_help()
