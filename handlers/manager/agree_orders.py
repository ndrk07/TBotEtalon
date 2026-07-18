from aiogram.fsm.context import FSMContext
from aiogram import Router, F
from aiogram.types import CallbackQuery
from filters.keysfabrick import ItemCallback
from keyboards.manager_keyboards import dynamic_watch_order_keyboard, agreed_order_keyboard, cancel_to_watch
from database.database import get_order_ids, get_order, change_status
from services.google_table import change_status_google_sheet

STATUS_NOTAGREE = "Отказано"
STATUS_AGREE = "Ожидание оплаты"

router = Router()

@router.callback_query(F.data.in_({"watch_orders", "cancel_to_watch_orders"}))
async def watch_orders(callback: CallbackQuery):
    order_ids = get_order_ids()
    await callback.message.edit_text("Выберите заявку:", reply_markup=dynamic_watch_order_keyboard(order_ids))
    await callback.answer()
@router.callback_query(ItemCallback.filter(F.action == "list_of_orders"))
async def processing_order(callback: CallbackQuery, callback_data: ItemCallback, state: FSMContext):
    order_id = callback_data.item_id
    order = get_order(order_id)
    await state.update_data(order=order)
    await show_order(callback, order)
    await callback.answer()
async def show_order(callback: CallbackQuery, data):
    await callback.message.edit_text(text=f"---- ЗАЯВКА № {data["order_id"]} ----\n"
                                  f"Имя: {data["name"]}\n"
                                  f"Контактный номер: {data["phone"]}\n"
                                  f"Продукт: {data["product"]}\n"
                                  f"Количество: {data["count"]}\n"
                                  f"Сумма: {data["sum_price"]}",
                                  reply_markup=agreed_order_keyboard())
#agree order
@router.callback_query(F.data == "agree_order_manager")
async def agree_order(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.bot.send_message(chat_id=user_data["order"]["telegram_id"], text=f"Заявка номер {user_data["order"]["order_id"]} принята, чек на оплату")
    change_status(user_data["order"]["order_id"], new_status=STATUS_AGREE)
    change_status_google_sheet(user_data["order"]["order_id"], STATUS_AGREE)
    await callback.message.edit_text(text="Заявка успешно принята", reply_markup=cancel_to_watch())
    await callback.answer()
#disagree order
@router.callback_query(F.data == "disagree_order_manager")
async def disagree_order(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    await callback.message.bot.send_message(chat_id=user_data["order"]["telegram_id"], text=f"Заявка номер {user_data["order"]["order_id"]} отклонена")
    change_status(user_data["order"]["order_id"], new_status=STATUS_NOTAGREE)
    change_status_google_sheet(user_data["order"]["order_id"], STATUS_NOTAGREE)
    await callback.message.edit_text(text="Отказ подтвержден", reply_markup=cancel_to_watch())
    await callback.answer()