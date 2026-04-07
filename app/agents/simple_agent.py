import re

from langchain_google_genai import ChatGoogleGenerativeAI

from app.core.config import get_settings
from app.models.chat import ChatMessage
from app.prompts.system_prompts import SYSTEM_PROMPT
from app.tools.calculator import calculator_tool
from app.tools.retriever import RetrieverTool, retrieval_tool
from app.schemas.chat import RouteDecision



class SimpleAgent:
    def __init__(self) -> None:
        settings = get_settings()
        self.model = ChatGoogleGenerativeAI(
            model=settings.GEMINI_MODEL,
            google_api_key=settings.GOOGLE_API_KEY,
            temperature=0.2,
        )
        self.retriever = RetrieverTool()
        self.tools = {
            "calculator": calculator_tool,
            "retriever": retrieval_tool,
        }


    def run(self, message: str, history: list[ChatMessage]) -> dict:
        route = self._classify_route(message)

        if route == "math":
            expression = self._extract_expression(message)
            if expression:
                result = self.tools["calculator"].invoke({"expression": expression})
                return {
                    "response": f"The calculated result is: {result}",
                    "sources": [],
                }

            return {
                "response": (
                    "I detected a math-related query, but I could not find a valid expression. "
                    "Please provide something like `12 + 7` or `100 / 4`."
                ),
                "sources": [],
            }

        if route == "retrieval":
            retrieved_docs = self.retriever.retrieve(message)
            if not retrieved_docs:
                return {
                    "response": "I could not find relevant knowledge for that question.",
                    "sources": [],
                }

            retrieval_context = "\n\n".join(
                f"Source: {doc.source}\nContent: {doc.content}"
                for doc in retrieved_docs
            )

            sources = [
                {
                    "source": doc.source,
                    "content": doc.content,
                }
                for doc in retrieved_docs
            ]

            prompt = (
                f"{SYSTEM_PROMPT}\n\n"
                "Use the retrieved context below to answer the user's question.\n"
                "If the answer is not supported by the context, say that clearly.\n\n"
                f"Retrieved context:\n{retrieval_context}\n\n"
                f"User question:\n{message}\n\n"
                "Provide a grounded answer based only on the retrieved context."
            )

            response = self.model.invoke(prompt)
            return {
                "response": response.content,
                "sources": sources,
            }

        prompt = self._build_prompt(message=message, history=history)
        response = self.model.invoke(prompt)
        return {
            "response": response.content,
            "sources": [],
        }
    
    def _classify_route(self, message: str) -> str:
        classifier = self.model.with_structured_output(RouteDecision)

        prompt = (
            "You are a routing classifier for an AI assistant.\n"
            "Decide the best route for the user query.\n\n"
            "Valid route values are:\n"
            "- direct\n"
            "- math\n"
            "- retrieval\n\n"
            "Rules:\n"
            "- Use 'math' if the query needs arithmetic or numerical calculation.\n"
            "- Use 'retrieval' if the query asks about a file, document, notes, policy, PDF, or knowledge base.\n"
            "- Otherwise use 'direct'.\n\n"
            f"User query: {message}"
        )

        result = classifier.invoke(prompt)

        if result.route in {"direct", "math", "retrieval"}:
            return result.route

        return "direct"

    def _build_prompt(self, message: str, history: list[ChatMessage]) -> str:
        history_text = "\n".join(
            f"{chat.role}: {chat.content}" for chat in history[-10:]
        )

        return (
            f"{SYSTEM_PROMPT}\n\n"
            f"Conversation history:\n{history_text}\n\n"
            f"User question:\n{message}\n\n"
            "Answer the user's question clearly and helpfully."
        )

    def _extract_expression(self, message: str) -> str | None:
        matches = re.findall(r"[0-9\.\+\-\*\/\(\)\%\s]+", message)
        candidates = [match.strip() for match in matches if match.strip()]
        if not candidates:
            return None
        return max(candidates, key=len)

    def _looks_like_math_question(self, message: str) -> bool:
        math_keywords = ["add", "sum", "multiply", "divide", "subtract", "+", "-", "*", "/"]
        lower_message = message.lower()
        return any(keyword in lower_message for keyword in math_keywords)

    def _looks_like_retrieval_question(self, message: str) -> bool:
        retrieval_keywords = ["document", "policy", "file", "notes", "pdf", "knowledge base"]
        lower_message = message.lower()
        return any(keyword in lower_message for keyword in retrieval_keywords)
