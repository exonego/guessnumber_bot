from random import randint

from aiogram.types import Message, CallbackQuery
from aiogram.enums import ContentType
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import TextInput, MessageInput

from app.state_groups.state_groups import StartSG
from app.business_logic.aux_funcs import num_check


# This handler reacts to click on no button
async def process_no_click(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    await callback.message.edit_text(
        text="Ладно(\nПришлите команду /start если все же решитесь."
    )

    await dialog_manager.done()


# This handler reacts to click on yes button
async def process_yes_click(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    dialog_manager.dialog_data.update(guessed=randint(1, 100), tryes=0, is_first=True)
    await dialog_manager.next()


# This handler reacts to input num
async def process_input_num(
    message: Message, widget: Button, dialog_manager: DialogManager, num: int
):
    dialog_manager.dialog_data.update(
        tryes=dialog_manager.dialog_data.get("tryes") + 1, is_first=False
    )
    if num == dialog_manager.dialog_data.get("guessed"):
        await message.reply(
            text="<b>Вы угадали!</b>\n"
            f"Количество использованных попыток: {dialog_manager.dialog_data.get("tryes")}\n\n"
            "Отправьте команду /start чтобы сыграть еще раз"
        )
        await dialog_manager.done()
    else:
        if num > dialog_manager.dialog_data.get("guessed"):
            await message.reply(text="Ваше число <i>больше</i> загаданного")
        else:
            await message.reply(text="Ваше число <i>меньше</i> загаданного")


# This handler reacts to invalid num
async def process_invalid_num(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    await message.reply(text="Некорректное число!")


# This handler reacts to not text
async def process_not_text(
    message: Message, widget: MessageInput, dialog_manager: DialogManager
):
    await message.reply(text="Это вовсе не текст!")


start_dialog = Dialog(
    Window(
        Const(
            text="Добро пожаловать в числовую угадайку!\n<b>Хотите сыграть?</b>",
        ),
        Row(
            Button(text=Const("Конечно!"), id="yes_button", on_click=process_yes_click),
            Button(text=Const("Нет!"), id="no_button", on_click=process_no_click),
        ),
        state=StartSG.start,
    ),
    Window(
        Const(
            text="Отлично! Я загадал случайное число в <b>интервале</b> [1; 100]",
            when="is_first",
        ),
        Const(
            text="Угадывайте, а я буду писать, ваше число больше или меньше загаданного"
        ),
        TextInput(
            id="first_num_input",
            type_factory=num_check,
            on_success=process_input_num,
            on_error=process_invalid_num,
        ),
        MessageInput(func=process_not_text, content_types=ContentType.ANY),
        state=StartSG.game,
    ),
)
