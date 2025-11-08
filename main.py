import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram_dialog import setup_dialogs

from config import load_config
from app.handlers.handlers import router

# Logger initialization
logger = logging.getLogger(__name__)


# Configuration and launching bot
async def main():
    # Loading config
    config = load_config()

    # Logging configuration
    logging.basicConfig(
        level=logging.getLevelName(level=config.log.level),
        format=config.log.format,
        style=config.log.style,
    )

    logger.info("Starting bot...")

    # Bot and dispatcher initialization
    bot = Bot(
        token=config.bot.token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    # Include routers
    dp.include_router(router)
    # Setting up dialogs
    setup_dialogs(dp)

    # Start polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
