from aiogram.utils.keyboard import InlineKeyboardBuilder
from filters.keysfabrick import ItemCallback

def build_dynamic_keyboard(products: list):
    builder = InlineKeyboardBuilder()
    for product in products:
        builder.button(text=product["name"], callback_data=ItemCallback(action="check_stocks", item_id=product["id"]))
    builder.button(text="В главное меню", callback_data="cancel_to_menu_manager")
    builder.adjust(1)
    return builder.as_markup()

def cancel_to_choice_product():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="cancel_to_product")
    return builder.as_markup()

def dynamic_watch_order_keyboard(order_ids: list):
    builder = InlineKeyboardBuilder()
    for id in order_ids:
        builder.button(text=f"№ {id}", callback_data=ItemCallback(action="list_of_orders", item_id=id))
    builder.button(text="В главное меню", callback_data="cancel_to_menu_manager")
    builder.adjust(1)
    return builder.as_markup()

def agreed_order_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="cancel_to_watch_orders")
    builder.button(text="Отказать", callback_data="disagree_order_manager")
    builder.button(text="Одобрить", callback_data="agree_order_manager")
    builder.adjust(2)
    return builder.as_markup()

def cancel_to_watch():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="cancel_to_watch_orders")
    return builder.as_markup()
def cancel_to_menu_manager():
    builder = InlineKeyboardBuilder()
    builder.button(text="В главное меню", callback_data="cancel_to_menu_manager")
    return builder.as_markup()