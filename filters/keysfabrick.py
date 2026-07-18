from aiogram.filters.callback_data import CallbackData

class ItemCallback(CallbackData, prefix="product"):
    action: str
    item_id: int