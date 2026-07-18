from aiogram import Router, F
from aiogram.types import CallbackQuery
from keyboards.manager_keyboards import cancel_to_choice_product, build_dynamic_keyboard
from filters.manager import IsManager
from filters.keysfabrick import ItemCallback
from services.get import service
from aiogram.fsm.context import FSMContext
from config import prName, prEd, prOst

router = Router()

@router.callback_query(F.data.in_({"check_stocks", "cancel_to_product"}))
async def warehouse_balances(callback: CallbackQuery):
    await callback.message.edit_text("Выберите товар:", reply_markup=build_dynamic_keyboard(service.get_products()))
    await callback.answer()
@router.callback_query(ItemCallback.filter(F.action == "check_stocks"))
async def stock_product(callback: CallbackQuery, state: FSMContext, callback_data: ItemCallback):
    product_id = callback_data.item_id
    product = service.get_product(product_id)
    await state.update_data(product=product)
    await show_stocks(callback, product)
    await callback.answer()
async def show_stocks(callback, p):
    await callback.message.edit_text(
        f"Продукт: {p[prName]}\n"
        f"Остаток на складе: {p[prOst]} {p[prEd]}",
        reply_markup=cancel_to_choice_product()
    )