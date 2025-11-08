from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode


from app.state_groups.state_groups import StartSG
from app.dialogs.start_dialog import start_dialog


# Include dialog
router = Router()
router.include_router(start_dialog)


# This handler reacts to the start command
@router.message(CommandStart())
async def process_command_start(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(state=StartSG.start, mode=StartMode.RESET_STACK)
