from app.agents.simple_agent import SimpleAgent
from app.repositories.chat_repository import ChatRepository
from app.schemas.chat import ChatRequest, ChatResponse


class ChatService:
    def __init__(self, chat_repository: ChatRepository) -> None:
        self.chat_repository = chat_repository
        self.agent = SimpleAgent()

    def process_chat(self, payload: ChatRequest) -> ChatResponse:
        self.chat_repository.create_message(
            session_id=payload.session_id,
            role="user",
            content=payload.message,
        )

        history = self.chat_repository.get_messages_by_session(payload.session_id)

        agent_result = self._generate_response(
            message=payload.message,
            history=history,
        )

        self.chat_repository.create_message(
            session_id=payload.session_id,
            role="assistant",
            content=agent_result["response"],
        )

        return ChatResponse(
            session_id=payload.session_id,
            response=agent_result["response"],
            sources=agent_result["sources"],
        )

    def _generate_response(self, message: str, history: list) -> dict:
        return self.agent.run(message=message, history=history)
