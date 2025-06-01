from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models import Message, Chat
from app.schemas import MessageRead
from datetime import datetime
from typing import Dict, List
from jose import JWTError, jwt
from app.utils import SECRET_KEY, ALGORITHM
import logging

router = APIRouter()

active_connections: Dict[int, List[WebSocket]] = {}
logger = logging.getLogger(__name__)

@router.websocket("/ws/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: int, token: str = None, db: AsyncSession = Depends(get_db)):
    await websocket.accept()
    # Проверка токена
    if token is None:
        logger.warning("WebSocket: отсутствует токен авторизации")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id = int(payload.get("sub"))
    except JWTError:
        logger.warning("WebSocket: неверный токен авторизации")
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
    logger.info(f"WebSocket: пользователь {user_id} подключился к чату {chat_id}")
    if chat_id not in active_connections:
        active_connections[chat_id] = []
    active_connections[chat_id].append(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            action = data.get("action")
            if action == "send_message":
                text = data.get("text")
                sender_id = user_id
                # Предотвращение дублей: ищем последнее сообщение с тем же текстом и отправителем
                last_msg = await db.execute(
                    """
                    SELECT * FROM messages WHERE chat_id=:chat_id AND sender_id=:sender_id ORDER BY timestamp DESC LIMIT 1
                    """,
                    {"chat_id": chat_id, "sender_id": sender_id}
                )
                last = last_msg.first()
                if last and last[0]["text"] == text:
                    continue  # дублирование
                msg = Message(chat_id=chat_id, sender_id=sender_id, text=text, timestamp=datetime.utcnow(), read=False)
                db.add(msg)
                await db.commit()
                await db.refresh(msg)
                response = MessageRead.from_orm(msg).dict()
                # Отправляем всем в чате
                for ws in active_connections[chat_id]:
                    await ws.send_json(response)
            elif action == "read_message":
                message_id = data.get("message_id")
                # Обновляем статус 'прочитано' для сообщения
                msg = await db.get(Message, message_id)
                if msg and msg.chat_id == chat_id:
                    msg.read = True
                    await db.commit()
                    await db.refresh(msg)
                    # Уведомляем отправителя, если он онлайн
                    for ws in active_connections[chat_id]:
                        await ws.send_json({"event": "read", "message_id": message_id, "reader_id": user_id})
    except WebSocketDisconnect:
        active_connections[chat_id].remove(websocket) 