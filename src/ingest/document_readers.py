import os
from pathlib import Path
from typing import Any, List, TYPE_CHECKING


if TYPE_CHECKING:
    from langchain.docstore.document import Document as LCDocument

from llama_index.core import Document
from llama_index.core.readers.base import BaseReader
from llama_index.readers.file.flat import FlatReader
from llama_index.core.node_parser import MarkdownNodeParser, MarkdownElementNodeParser
from llama_index.core.schema import Document


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

                    if load_kwargs.get("reader") == "markdown":
                        content = MarkdownNodeParser().load_data(Path(filepath))

                        for doc in content:
                            doc.metadata = {"filename": filename, "extenstion": ".md"}
                            doc.text = doc.text.replace("\x00", "")
                    else:
                        content = FlatReader().load_data(Path(filepath))
                        for doc in content:
                            doc.text = doc.text.replace("\x00", "")

                    docs.extend(content)

        return docs

    def load_langchain_documents(self, **load_kwargs: Any) -> List["LCDocument"]:
        """Load data in LangChain document format."""
        docs = self.load_data(**load_kwargs)
        return [d.to_langchain_format() for d in docs]
