@echo off
REM Скрипт для запуска проекта WinDI Chat в один клик
cd /d %~dp0
echo Запуск Docker Compose...
docker-compose up --build
pause 