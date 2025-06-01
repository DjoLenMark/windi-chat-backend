from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Message, Chat, User
from app.schemas import MessageRead, UserCreate, UserRead, ChatCreate, ChatRead, Token
from app.utils import get_password_hash, verify_password, create_access_token
from sqlalchemy.future import select
from typing import List
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from app.deps import get_current_user
from app.repositories.chat_repository import ChatRepository
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/history/{chat_id}", response_model=List[MessageRead])
async def get_history(
    chat_id: int,
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Message).where(Message.chat_id == chat_id).order_by(Message.timestamp.asc()).offset(offset).limit(limit)
    )
    messages = result.scalars().all()
    return messages

@router.post("/register", response_model=UserRead)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).where(User.email == user.email))
    if db_user.scalar_one_or_none():
        logger.warning(f"Попытка регистрации с уже существующим email: {user.email}")
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    logger.info(f"Зарегистрирован новый пользователь: {user.email}")
    return new_user

@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    db_user = await db.execute(select(User).where(User.email == form_data.username))
    user = db_user.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/", response_model=UserRead)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    db_user = await db.execute(select(User).where(User.email == user.email))
    if db_user.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already registered")
    hashed_password = get_password_hash(user.password)
    new_user = User(name=user.name, email=user.email, password=hashed_password)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/chats/", response_model=ChatRead)
async def create_chat(chat: ChatCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    new_chat = Chat(name=chat.name, type=chat.type)
    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return new_chat

@router.post("/groups/{group_id}/add_user/{user_id}")
async def add_user_to_group(group_id: int, user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ChatRepository(db)
    group = await repo.add_user_to_group(group_id, user_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group or user not found")
    return {"status": "user added", "group_id": group_id, "user_id": user_id}

@router.post("/groups/{group_id}/remove_user/{user_id}")
async def remove_user_from_group(group_id: int, user_id: int, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    repo = ChatRepository(db)
    group = await repo.remove_user_from_group(group_id, user_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group or user not found")
    return {"status": "user removed", "group_id": group_id, "user_id": user_id} 
 