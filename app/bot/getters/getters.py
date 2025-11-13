from aiogram_dialog import DialogManager


async def get_data(dialog_manager: DialogManager, **kwargs):
    return {
        "is_first": dialog_manager.dialog_data.get("is_first"),
        "tryes": dialog_manager.dialog_data.get("tryes"),
        "result": dialog_manager.dialog_data.get("result"),
        "invalid": dialog_manager.dialog_data.get("invalid"),
    }
