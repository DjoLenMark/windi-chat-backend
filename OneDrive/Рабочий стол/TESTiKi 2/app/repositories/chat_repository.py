from sqlalchemy.ext.asyncio import AsyncSession
from app.models import Chat, Message, Group, User
from sqlalchemy.future import select
from typing import List

class ChatRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_chat(self, chat_id: int) -> Chat:
        result = await self.db.execute(select(Chat).where(Chat.id == chat_id))
        return result.scalar_one_or_none()

    async def get_messages(self, chat_id: int, limit: int = 20, offset: int = 0) -> List[Message]:
        result = await self.db.execute(
            select(Message).where(Message.chat_id == chat_id).order_by(Message.timestamp.asc()).offset(offset).limit(limit)
        )
        return result.scalars().all()

    async def add_user_to_group(self, group_id: int, user_id: int):
        """Добавить пользователя в группу."""
        group = await self.db.get(Group, group_id)
        user = await self.db.get(User, user_id)
        if group and user:
            group.participants.append(user)
            await self.db.commit()
            await self.db.refresh(group)
        return group

    async def remove_user_from_group(self, group_id: int, user_id: int):
        """Удалить пользователя из группы."""
        group = await self.db.get(Group, group_id)
        user = await self.db.get(User, user_id)
        if group and user and user in group.participants:
            group.participants.remove(user)
            await self.db.commit()
            await self.db.refresh(group)
        return group 