import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.controllers import rest, ws

app = FastAPI(title="WinDI Chat")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

app.include_router(rest.router)
app.include_router(ws.router) 