# WinDI Chat — Backend

## Описание

WinDI Chat — это асинхронный backend для мессенджера с поддержкой групповых чатов, обмена сообщениями в реальном времени (WebSocket), хранением истории в PostgreSQL и JWT-авторизацией. Проект полностью покрывает требования технического задания для позиции Senior Backend-разработчика.

---

## Стек технологий
- Python 3.10+
- FastAPI (REST + WebSocket)
- SQLAlchemy (async)
- PostgreSQL
- Docker, Docker Compose
- Swagger/OpenAPI
- JWT (OAuth2)
- Pytest (тесты)

---

## Быстрый старт

1. Клонируйте репозиторий:
   ```bash
   git clone <ВАША_ССЫЛКА_НА_GITHUB>
   cd windi-chat-backend
   ```
2. Запустите проект через Docker Compose:
   ```bash
   docker-compose up --build
   ```
   FastAPI будет доступен на [http://localhost:8000/docs](http://localhost:8000/docs)

3. (Опционально) Выполните миграции:
   ```bash
   docker-compose exec backend alembic upgrade head
   ```

4. Для быстрого запуска на Windows используйте файл `run_all.bat` (двойной клик).

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
  "password": "pass1234"
}
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

```bash
docker-compose exec backend pytest
```

---

## PEP8 и качество кода
- Весь код приведён к стандарту PEP8
- Используются docstring и комментарии
- Логика разделена на слои (controllers, services, repositories)

---

## Публикация на GitHub
1. Создайте репозиторий на GitHub (например, windi-chat-backend)
2. Выполните:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: full solution for WinDI Chat"
   git branch -M main
   git remote add origin https://github.com/ВАШ_ЛОГИН/ВАШ_РЕПОЗИТОРИЙ.git
   git push -u origin main
   ```

---

## Контакты и поддержка
Вопросы — в Issues или на email: your@email.com

---

**Проект полностью соответствует техническому заданию и готов к использованию!** 