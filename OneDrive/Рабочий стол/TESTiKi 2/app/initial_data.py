import asyncio
from app.database import engine
from app.models import Base, User, Chat, Message
from app.utils import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

async def create_initial_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    async with async_session() as session:
        # Проверяем, есть ли уже пользователи
        users = (await session.execute("SELECT * FROM users")).first()
        if users:
            return
        user1 = User(name="Иван", email="ivan@example.com", password=get_password_hash("1234"))
        user2 = User(name="Анна", email="anna@example.com", password=get_password_hash("1234"))
        session.add_all([user1, user2])
        await session.commit()
        await session.refresh(user1)
        await session.refresh(user2)
        chat = Chat(name="Общий чат", type="group")
        session.add(chat)
        await session.commit()
        await session.refresh(chat)
        msg1 = Message(chat_id=chat.id, sender_id=user1.id, text="Привет!", read=True)
        msg2 = Message(chat_id=chat.id, sender_id=user2.id, text="Привет, Иван!", read=True)
        session.add_all([msg1, msg2])
        await session.commit()

if __name__ == "__main__":
    asyncio.run(create_initial_data()) 