from app.repositories.chat_repository import ChatRepository
from app.models import Message
from typing import List

class ChatService:
    def __init__(self, chat_repo: ChatRepository):
        self.chat_repo = chat_repo

    async def get_chat_history(self, chat_id: int, limit: int = 20, offset: int = 0) -> List[Message]:
        return await self.chat_repo.get_messages(chat_id, limit, offset) 