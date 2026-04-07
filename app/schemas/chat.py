from datetime import datetime

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    session_id: str = Field(..., min_length=1, max_length=100)
    message: str = Field(..., min_length=1)


class SourceItem(BaseModel):
    source: str
    content: str


class ChatResponse(BaseModel):
    session_id: str
    response: str
    sources: list[SourceItem] = []


class RouteDecision(BaseModel):
    route: str


class ChatMessageRead(BaseModel):
    id: int
    session_id: str
    role: str
    content: str
    created_at: datetime

    model_config = {
        "from_attributes": True,
    }
