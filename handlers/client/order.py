from aiogram import Router, F
import re
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove
from filters.keysfabrick import ItemCallback
from aiogram.fsm.context import FSMContext
from states.order import OrderState
from services.get import service
from services.calculation import calculatePrice
from keyboards.order_keyboard import main_menu_client_keyboard, cancel_to_choiceName, cancel_to_choiceCount, cancel_to_choiceProduct, agreed_or_disagree, build_dynamic_keyboard, build_contact_keyboard
from config import prOst, prEd, prName, prPrice, MAIN_MANAGER
from services.google_table import new_order
from database.database import add_order

PHONE_REGEX = r"^\+?[1-9]\d{9,14}$"
router = Router()
#choice product
@router.callback_query(F.data.in_({"make_order", "cancel_to_choiceproduct"}))
async def choiceProduct(callback: CallbackQuery):
    await callback.message.edit_text("Выберите товар:", reply_markup=build_dynamic_keyboard(service.get_products()))
    await callback.answer()
#choice count
@router.callback_query(ItemCallback.filter(F.action == "create_order"))
async def chooseProduct(callback, state: FSMContext, callback_data: ItemCallback):
    product_id = callback_data.item_id
    product = service.get_product(product_id)
    await state.update_data(product=product)
    await state.set_state(OrderState.count)
    await show_choice_count(callback, product)
    await callback.answer()
async def show_choice_count(callback, product):
    await callback.message.edit_text(f"Напишите количество (в наличии {product[prOst]} {product[prEd]}):", reply_markup=cancel_to_choiceProduct())
#choice name
@router.message(OrderState.count)
async def chooseCount(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text.isdigit(): await message.answer("Количество должно быть числом"); return
    count = int(text)
    c = await state.get_data()
    max_count = c["product"][prOst]
    if count < 1: await message.answer("Количество должно быть больше 0"); return
    if count > max_count: await message.answer("На складе столько нет"); return
    
    await state.update_data(count=count)
    await state.set_state(OrderState.name)
    await message.answer("Как Вас зовут?",reply_markup=cancel_to_choiceCount())
#choice number
@router.message(OrderState.name)
async def chooseName(message: Message, state: FSMContext):
    text = message.text.strip()
    if text.isdigit(): await message.answer("Введите ваше имя"); return
    name = str(text)
    await state.update_data(name=name)
    await state.set_state(OrderState.phone)
    await message.answer("Введите номер телефона", reply_markup=build_contact_keyboard())
    await message.answer("Можно ввести вручную", reply_markup=cancel_to_choiceName())
#number + agreed
@router.message(OrderState.phone)
async def choosePhone(message: Message, state: FSMContext):
    if message.contact:
        if message.from_user.id != message.contact.user_id:
            await message.answer("Пожалуйста, отправьте свой контакт или введите номер вручную")
            return
        phone = message.contact.phone_number
    elif message.text:
        clean_text = re.sub(r"[\s\-() ]", "", message.text)
        if re.match(PHONE_REGEX, clean_text):
            phone = clean_text
        else: 
            await message.answer("Неверный формат номера")
            return
    if phone:
        await state.update_data(phone=phone)
        user_data = await state.get_data()
        await message.answer("Отправить заявку?", reply_markup=ReplyKeyboardRemove())
        await message.answer(show_order(user_data, "-"),  reply_markup=agreed_or_disagree())
def show_order(user_data, num):
    return (
        f"---- ЗАЯВКА НА ПОКУПКУ {num}---\n"
        f"Продукт: {user_data["product"][prName]}\n"
        f"Количество: {user_data["count"]}\n"
        f"Имя: {user_data["name"]}\n"
        f"Контактный номер: {user_data["phone"]}\n"
        f"Расчетная стоимость: {calculatePrice(user_data["product"][prPrice], user_data["count"])} руб"
    )
@router.callback_query(F.data == "agree_order_callback")
#agreed order
async def agreedOrder(callback: CallbackQuery, state:FSMContext):
    await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    await callback.message.edit_text("Отправляю заявку...")
    user_data = await state.get_data()
    order_id = add_order(callback.from_user.id, user_data)
    new_order(user_data, order_id)
    for target_id in MAIN_MANAGER:
        await callback.message.bot.send_message(chat_id=target_id, text=show_order(user_data, str(order_id) + " -"))
    await callback.message.answer("Заявка оформлена! Ожидайте звонка", reply_markup=main_menu_client_keyboard())
    await callback.answer()
#disagree order
@router.callback_query(F.data == "disagree_order_callback")
async def disagreeOrder(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await choiceProduct(callback)
    await callback.answer()
@router.callback_query(F.data == "cancel_to_choicecount")
async def cancelToChoiceCount(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.count)
    p = await state.get_data()
    await show_choice_count(callback, p["product"])
    await callback.answer()
@router.callback_query(F.data == "cancel_to_choicename")
async def cancelToChoiceName(callback: CallbackQuery, state: FSMContext):
    await state.set_state(OrderState.name)
    await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    await callback.message.edit_text("Как Вас зовут?",reply_markup=cancel_to_choiceCount())
    await callback.answer()
@router.callback_query(F.data == "cancel_to_choicephone")
async def cancelToPhone(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.bot.delete_message(chat_id=callback.message.chat.id, message_id=callback.message.message_id - 1)
    await callback.message.answer("Введите номер телефона", reply_markup=build_contact_keyboard())
    await callback.message.answer("Можно ввести вручную", reply_markup=cancel_to_choiceName())
    await callback.answer()