import pytest
from httpx import AsyncClient
from app.main import app
import asyncio
import json
from fastapi.testclient import TestClient
from websockets import connect as ws_connect

@pytest.mark.asyncio
async def test_create_user_and_chat():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Создание пользователя
        resp = await ac.post("/users/", json={"name": "Test", "email": "test@example.com", "password": "1234"})
        assert resp.status_code == 200
        user = resp.json()
        # Создание чата
        resp = await ac.post("/chats/", json={"name": "Test Chat", "type": "group"})
        assert resp.status_code == 200
        chat = resp.json()
        # История сообщений (пустая)
        resp = await ac.get(f"/history/{chat['id']}")
        assert resp.status_code == 200
        assert resp.json() == []

@pytest.mark.asyncio
async def test_register_and_login():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Регистрация
        resp = await ac.post("/register", json={"name": "TestUser", "email": "testuser@example.com", "password": "pass1234"})
        assert resp.status_code == 200
        # Логин
        resp = await ac.post("/login", data={"username": "testuser@example.com", "password": "pass1234"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        # Создание чата
        headers = {"Authorization": f"Bearer {token}"}
        resp = await ac.post("/chats/", json={"name": "Test Chat", "type": "group"}, headers=headers)
        assert resp.status_code == 200
        chat = resp.json()
        # История сообщений (пустая)
        resp = await ac.get(f"/history/{chat['id']}", headers=headers)
        assert resp.status_code == 200
        assert resp.json() == []

@pytest.mark.asyncio
async def test_read_status_websocket():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Регистрация и логин
        resp = await ac.post("/register", json={"name": "WSUser", "email": "wsuser@example.com", "password": "ws1234"})
        assert resp.status_code == 200
        resp = await ac.post("/login", data={"username": "wsuser@example.com", "password": "ws1234"})
        assert resp.status_code == 200
        token = resp.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}
        # Создание чата
        resp = await ac.post("/chats/", json={"name": "WS Chat", "type": "group"}, headers=headers)
        assert resp.status_code == 200
        chat_id = resp.json()["id"]
        # Получаем URL WebSocket
        ws_url = f"ws://localhost:8000/ws/{chat_id}?token={token}"
        # Подключаемся к WebSocket
        import websockets
        async with websockets.connect(ws_url) as ws:
            # Отправляем сообщение
            await ws.send(json.dumps({"action": "send_message", "text": "hello from ws"}))
            msg = await ws.recv()
            msg_data = json.loads(msg)
            assert msg_data["text"] == "hello from ws"
            # Отмечаем как прочитанное
            await ws.send(json.dumps({"action": "read_message", "message_id": msg_data["id"]}))
            read_event = await ws.recv()
            read_data = json.loads(read_event)
            assert read_data["event"] == "read"
            assert read_data["message_id"] == msg_data["id"] 