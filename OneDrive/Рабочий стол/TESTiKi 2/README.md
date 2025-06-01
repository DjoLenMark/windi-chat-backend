# 💬 WinDI Chat — Асинхронный групповой мессенджер на FastAPI

> Тестовое задание для позиции Senior Backend-разработчика в компанию **WinDI**

WinDI Chat — это мини-мессенджер, реализованный на FastAPI с поддержкой WebSocket, REST API, асинхронной работой и Docker-контейнеризацией. Приложение позволяет обмениваться сообщениями в реальном времени, создавать групповые чаты и получать историю сообщений из базы данных PostgreSQL.

---

## 🚀 Быстрый старт

   ```
   FastAPI будет доступен на [http://localhost:8000/docs](http://localhost:8000/docs)

 (Опционально) Выполните миграции:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

 Для быстрого запуска на Windows используйте файл `run_all.bat` (двойной клик).

---

## Структура базы данных
- users: id, имя, email, пароль (хэш)
- chats: id, название, тип (private/group)
- groups: id, название, создатель, участники
- messages: id, chat_id, sender_id, text, timestamp, read

---

## Основные возможности
- JWT-авторизация (регистрация, логин, защита всех эндпоинтов и WebSocket)
- WebSocket: обмен сообщениями, статус "прочитано", предотвращение дублей, поддержка нескольких устройств
- REST API: история сообщений, создание чатов, управление участниками групп
- Логирование всех ключевых событий
- Тесты (Pytest) для всех основных функций

---

## Примеры API

### Регистрация пользователя
```http
POST /register
{
  "name": "User",
  "email": "user@example.com",
  "password": "pass1234"}
```
### Логин и получение JWT
```http
POST /login
Content-Type: application/x-www-form-urlencoded
username=user@example.com&password=pass1234
```
### WebSocket
```
ws://localhost:8000/ws/{chat_id}?token=ВАШ_JWT
```
### Управление группами
- Добавить пользователя: `POST /groups/{group_id}/add_user/{user_id}`
- Удалить пользователя: `POST /groups/{group_id}/remove_user/{user_id}`
---
## Тестирование
---
## PEP8 и качество кода
- Весь код приведён к стандарту PEP8
- Используются docstring и комментарии
- Логика разделена на слои (controllers, services, repositories)
---
**Проект полностью соответствует техническому заданию и готов к использованию!** 