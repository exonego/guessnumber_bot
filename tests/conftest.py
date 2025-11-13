from unittest.mock import Mock

import pytest
from aiogram import Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Chat, User
from aiogram.enums import ChatType
from aiogram_dialog import setup_dialogs
from aiogram_dialog.test_tools import BotClient, MockMessageManager

from app.bot.handlers.handlers import router


@pytest.fixture(scope="session")
def performers() -> dict[str, Dispatcher | BotClient | MockMessageManager]:
    usecase = Mock()
    user_getter = Mock(side_effect=["Username"])
    dp = Dispatcher(
        usecase=usecase,
        user_getter=user_getter,
        storage=MemoryStorage(),
    )
    client = BotClient(dp)
    message_manager = MockMessageManager()
    dp.include_router(router)
    setup_dialogs(dp, message_manager=message_manager)
    return {"client": client, "message_manager": message_manager}
