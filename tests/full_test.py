import pytest
from aiogram.types import InlineKeyboardMarkup
from aiogram_dialog.test_tools import BotClient, MockMessageManager
from aiogram_dialog.test_tools.keyboard import InlineButtonTextLocator


@pytest.mark.asyncio
async def test_dialog(performers, monkeypatch):
    monkeypatch.setattr("app.bot.dialogs.start_dialog.randint", lambda x, y: 42)
    client: BotClient = performers["client"]
    message_manager: MockMessageManager = performers["message_manager"]

    # Start
    await client.send("/start")

    first_message = message_manager.one_message()
    assert "Добро пожаловать в числовую угадайку!" in first_message.text
    assert first_message.reply_markup
    assert isinstance(first_message.reply_markup, InlineKeyboardMarkup)
    assert first_message.reply_markup.inline_keyboard[0][0].text == "Конечно!"
    assert first_message.reply_markup.inline_keyboard[0][1].text == "Нет!"

    # Redraw
    message_manager.reset_history()
    await client.send("hi!")

    first_message = message_manager.one_message()
    assert "Добро пожаловать в числовую угадайку!" in first_message.text

    # Click yes
    message_manager.reset_history()
    callback_id = await client.click(first_message, InlineButtonTextLocator("Конечно!"))

    message_manager.assert_answered(callback_id)
    second_message = message_manager.one_message()
    assert "Отлично!" in second_message.text

    # Not num
    message_manager.reset_history()
    await client.send("d")

    not_num_message = message_manager.one_message()
    assert not_num_message.text == "Некорректное число!"

    # Wrong guess
    message_manager.reset_history()
    await client.send("1")

    wrong_message = message_manager.one_message()
    assert "Ваше число" in wrong_message.text

    # Right guess
    message_manager.reset_history()
    await client.send("42")

    right_message = message_manager.first_message()
    assert "Вы угадали!" in right_message.text
