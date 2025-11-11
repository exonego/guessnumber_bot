from datetime import datetime

import pytest
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.enums import ChatType
from aiogram.methods import SendMessage
from aiogram.methods.base import TelegramType
from aiogram.types import (
    Update,
    Chat,
    User,
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)


@pytest.mark.asyncio
async def test_cmd_start(dp, bot):
    chat = Chat(id=1234567, type=ChatType.PRIVATE)

    mock_message = Message(message_id=2, date=datetime.now(), chat=chat, text="test")
    bot.add_result_for(method=SendMessage, ok=True, result=mock_message)

    user = User(id=1234567, is_bot=False, first_name="User")
    message = Message(
        message_id=1, chat=chat, from_user=user, text="/start", date=datetime.now()
    )

    result = await dp.feed_update(bot, Update(message=message, update_id=1))
    assert result is not UNHANDLED
    outgoing_message: TelegramType = bot.get_request()
    assert isinstance(outgoing_message, SendMessage)
    assert (
        outgoing_message.text
        == "Добро пожаловать в числовую угадайку!\n<b>Хотите сыграть?</b>"
    )
    assert outgoing_message.reply_markup is not None
    markup = outgoing_message.reply_markup
    assert isinstance(markup, InlineKeyboardMarkup)
    button_1: InlineKeyboardButton = markup.inline_keyboard[0][0]
    button_2: InlineKeyboardButton = markup.inline_keyboard[0][1]
    assert button_1.text == "Конечно!"
    assert button_2.text == "Нет!"
