from aiogram import F, Router, html
from aiogram.types import CallbackQuery
from aiogram.enums import ParseMode
from keyboards.manager_keyboards import cancel_to_menu_manager
from database.database import get_week_orders

router = Router()

@router.callback_query(F.data == "week_report")
async def weekly_report(callback: CallbackQuery):
    dictionary = get_week_orders()
    await callback.message.edit_text(show_weekly_report(dictionary), reply_markup=cancel_to_menu_manager(), parse_mode=ParseMode.HTML)
    await callback.answer()
def show_weekly_report(dictionary):
    logs = [html.code(f"{"ID".ljust(3)} | {"Имя".ljust(15)} | {"Сумма".ljust(8)} | {"Статус".ljust(15)}")]
    for d in dictionary:
        id_str = str(d["order_id"]).ljust(3)
        name_str = str(d["name"]).ljust(15)
        price_str = str(d["sum_price"]).ljust(8)
        status_str = str(d["status"]).ljust(15)
        line = f"{id_str} | {name_str} | {price_str} | {status_str}"
        logs.append(html.code(line))
    return "\n".join(logs)
    