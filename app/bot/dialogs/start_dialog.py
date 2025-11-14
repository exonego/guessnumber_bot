from random import randint

from aiogram.types import Message, CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format, Multi
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog.widgets.input import TextInput, MessageInput

from app.bot.state_groups.state_groups import StartSG
from app.bot.getters.getters import get_data
from app.business_logic.aux_funcs import num_check


async def process_no_click(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    """Reacts to click on no-button"""

    await dialog_manager.switch_to(StartSG.denied)
    await dialog_manager.show()
    await dialog_manager.done()


async def process_yes_click(
    callback: CallbackQuery, widget: Button, dialog_manager: DialogManager
):
    """Reacts to click on yes button"""

    dialog_manager.dialog_data.update(guessed=randint(1, 100), tryes=0, is_first=True)
    await dialog_manager.next()


async def process_input_num(
    message: Message, widget: Button, dialog_manager: DialogManager, num: int
):
    """Reacts to input num"""

    dialog_manager.dialog_data.update(
        tryes=dialog_manager.dialog_data.get("tryes") + 1, is_first=False
    )
    if num == dialog_manager.dialog_data.get("guessed"):
        await dialog_manager.next()
        await dialog_manager.show()
        await dialog_manager.done()

    else:
        if num > dialog_manager.dialog_data.get("guessed"):
            dialog_manager.dialog_data.update(
                result="Ваше число <i>больше</i> загаданного", invalid=False
            )
        else:
            dialog_manager.dialog_data.update(
                result="Ваше число <i>меньше</i> загаданного", invalid=False
            )


async def process_invalid_num(
    message: Message,
    widget: TextInput,
    dialog_manager: DialogManager,
    error: ValueError,
):
    """Reacts to invalid num"""

    dialog_manager.dialog_data.update(is_first=False, result=None, invalid=True)


# dialog
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
            text="Отлично! Я загадал случайное число в <b>интервале</b> [1; 100]\n"
            "Угадывайте, а я буду писать, ваше число больше или меньше загаданного",
            when="is_first",
        ),
        Format(text="{result}", when="result"),
        Const(text="Некорректное число!", when="invalid"),
        TextInput(
            id="first_num_input",
            type_factory=num_check,
            on_success=process_input_num,
            on_error=process_invalid_num,
        ),
        state=StartSG.game,
        getter=get_data,
    ),
    Window(
        Format(
            text="<b>Вы угадали!</b>\n"
            "Количество использованных попыток: {tryes}\n\n"
            "Отправьте команду /start чтобы сыграть еще раз"
        ),
        state=StartSG.win,
        getter=get_data,
    ),
    Window(
        Const(text="Ладно(\nПришлите команду /start если все же решитесь."),
        state=StartSG.denied,
    ),
)
