from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Router, F
from filters.manager import IsManager
from keyboards.start_keyboard import client_keyboard, manager_keyboard

router = Router()

@router.message(CommandStart(), IsManager())
async def managerStart(message: Message):
    await message.answer("Приветствую! Меню Менеджера:", reply_markup=manager_keyboard())

@router.callback_query(F.data == "cancel_to_menu_manager", IsManager())
async def cancel_to_menuManager(callback):
    await callback.message.delete()
    await managerStart(callback.message)
    await callback.answer()

@router.message(CommandStart())
async def clientStart(message: Message):
    await message.answer("Приветствую! Клиентское меню:", reply_markup=client_keyboard())

@router.callback_query(F.data == "cancel_to_menu_client")
async def cancel_to_menuClient(callback):
    await callback.message.delete()
    await clientStart(callback.message)
    await callback.answer()