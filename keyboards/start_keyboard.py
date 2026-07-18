from aiogram.utils.keyboard import InlineKeyboardBuilder

def client_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Сделать заказ", callback_data="make_order")
    return builder.as_markup()

def manager_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Проверить остатки", callback_data="check_stocks")
    builder.button(text="Просмотр заявок", callback_data="watch_orders")
    builder.button(text="Недельный отчет", callback_data="week_report")
    builder.adjust(1)
    return builder.as_markup()