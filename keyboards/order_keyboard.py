from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from filters.keysfabrick import ItemCallback

def build_dynamic_keyboard(products: list):
    choice_product_keyboard = InlineKeyboardBuilder()
    for product in products:
        choice_product_keyboard.button(text=product["name"], callback_data=ItemCallback(action="create_order", item_id=product["id"]))
    choice_product_keyboard.button(text="В главное меню", callback_data="cancel_to_menu_client")
    choice_product_keyboard.adjust(1)
    return choice_product_keyboard.as_markup()

def  build_contact_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.button(text="Отправить свой номер", request_contact=True)
    return builder.as_markup(resize_keyboard=True)

def agreed_or_disagree():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="cancel_to_choicephone")
    builder.button(text="Сбросить", callback_data="disagree_order_callback")
    builder.button(text="Подтвердить", callback_data="agree_order_callback")
    builder.adjust(2)
    return builder.as_markup()

def cancel_to_choiceProduct():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="cancel_to_choiceproduct")
    return builder.as_markup()
def cancel_to_choiceCount():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="cancel_to_choicecount")
    return builder.as_markup()
def cancel_to_choiceName():
    builder = InlineKeyboardBuilder()
    builder.button(text="Назад", callback_data="cancel_to_choicename")
    return builder.as_markup()
def main_menu_client_keyboard():
    builder = InlineKeyboardBuilder()
    builder.button(text="В главное меню", callback_data="cancel_to_menu_client")
    return builder.as_markup()