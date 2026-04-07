from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.chat import ChatMessage


class ChatRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_message(self, session_id: str, role: str, content: str) -> ChatMessage:
        message = ChatMessage(
            session_id=session_id,
            role=role,
            content=content,
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message

    def get_messages_by_session(self, session_id: str) -> list[ChatMessage]:
        stmt = (
            select(ChatMessage)
            .where(ChatMessage.session_id == session_id)
            .order_by(ChatMessage.created_at.asc(), ChatMessage.id.asc())
        )
        return list(self.db.scalars(stmt).all())
