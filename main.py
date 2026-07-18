import asyncio
from aiogram import Bot, Dispatcher
from config import TOKEN
from aiogram.client.session.aiohttp import AiohttpSession
from services.get import service
from handlers.start import router as start_router
from handlers.client.order import router as client_router
from handlers.manager.check import router as manager_router
from handlers.manager.agree_orders import router as manager_router_watch
from handlers.manager.week_report import router as manager_router_week
from database.database import init_db

proxyURL = "http://127.0.0.1:10808"
session = AiohttpSession(proxy=proxyURL)

async def main():
    bot = Bot(TOKEN, session=session)
    dp = Dispatcher()
    service.refresh()
    init_db()

    dp.include_router(start_router)
    dp.include_router(client_router)
    dp.include_router(manager_router)
    dp.include_router(manager_router_watch)
    dp.include_router(manager_router_week)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())