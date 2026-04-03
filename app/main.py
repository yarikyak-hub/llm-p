from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine

# Импортируем роутеров
from app.api import routes_auth, routes_chat

def create_app() -> FastAPI:
    """
    Создаём функцию, обеспечивающую работу Веб-сервиса
    """
    app = FastAPI(
        title = 'Мой ЛЛМ проект'
    )

    # Подключаем роутеры
    app.include_router(routes_auth.router, )
    app.include_router(routes_chat.router, )

    # Создание таблиц в БД при запуске приложения
    @app.on_event('startup')
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    # Возращает статус и окружение сервера, если он запущен
    @app.get("/health")
    async def health_check():
        return {
            "status": "ok",
            "environment": "development"
        }
    return app

app = create_app()

