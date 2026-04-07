from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.vectorstore.chroma_store import ChromaVectorStore


class VectorService:
    def __init__(self) -> None:
        self.vector_store = ChromaVectorStore()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500,
            chunk_overlap=50,
        )

    def load_text_documents_from_directory(self, directory: str, reset: bool = False) -> None:
        if reset:
            self.vector_store.reset_collection()

        path = Path(directory)
        documents = []

        for file_path in path.glob("*.txt"):
            text = file_path.read_text(encoding="utf-8")
            documents.append(
                Document(
                    page_content=text,
                    metadata={"source": str(file_path)},
                )
            )

        if not documents:
            return

        chunks = self.text_splitter.split_documents(documents)
        self.vector_store.add_documents(chunks)
