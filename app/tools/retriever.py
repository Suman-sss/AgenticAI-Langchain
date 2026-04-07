from dataclasses import dataclass

from langchain_core.tools import tool

from app.vectorstore.chroma_store import ChromaVectorStore


@dataclass
class RetrievedDocument:
    content: str
    source: str


class RetrieverTool:
    def __init__(self) -> None:
        self.vector_store = ChromaVectorStore()

    def retrieve(self, query: str) -> list[RetrievedDocument]:
        documents = self.vector_store.similarity_search(query=query, k=3)

        results = []
        for doc in documents:
            results.append(
                RetrievedDocument(
                    content=doc.page_content,
                    source=doc.metadata.get("source", "unknown"),
                )
            )

        return results


@tool
def retrieval_tool(query: str) -> str:
    """
    Retrieve relevant knowledge from the vector database for questions
    about files, documents, notes, policies, PDFs, or the knowledge base.
    """
    retriever = RetrieverTool()
    results = retriever.retrieve(query)

    if not results:
        return "No relevant knowledge was found."

    return "\n\n".join(
        f"Source: {item.source}\nContent: {item.content}"
        for item in results
    )
