from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    name: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int
    class Config:
        orm_mode = True

class ChatBase(BaseModel):
    name: str
    type: str  # private/group

class ChatCreate(ChatBase):
    pass

class ChatRead(ChatBase):
    id: int
    class Config:
        orm_mode = True

class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    creator_id: int
    participant_ids: List[int]

class GroupRead(GroupBase):
    id: int
    creator_id: int
    participant_ids: List[int]
    class Config:
        orm_mode = True

class MessageBase(BaseModel):
    text: str

class MessageCreate(MessageBase):
    chat_id: int
    sender_id: int

class MessageRead(MessageBase):
    id: int
    chat_id: int
    sender_id: int
    timestamp: datetime
    read: bool
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: Optional[int] = None 