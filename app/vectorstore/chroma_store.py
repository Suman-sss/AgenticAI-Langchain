from langchain_chroma import Chroma
from langchain_core.documents import Document

from app.core.config import get_settings
from app.services.embedding_service import EmbeddingService


class ChromaVectorStore:
    def __init__(self) -> None:
        settings = get_settings()
        embedding_service = EmbeddingService()
        self.collection_name = "agentic_beginner_knowledge"

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=embedding_service.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        )

    def add_documents(self, documents: list[Document]) -> None:
        self.vector_store.add_documents(documents)

    def similarity_search(self, query: str, k: int = 3) -> list[Document]:
        results = self.vector_store.similarity_search_with_relevance_scores(query, k=k)
        filtered = [doc for doc, score in results if score >= 0.5]
        return filtered

    def reset_collection(self) -> None:
        self.vector_store.delete_collection()
        settings = get_settings()
        embedding_service = EmbeddingService()
        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=embedding_service.embeddings,
            persist_directory=settings.CHROMA_PERSIST_DIRECTORY,
        )
