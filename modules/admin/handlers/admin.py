from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, BufferedInputFile

from modules.admin.middlewares import AdminOnlyMiddleware


admin_rt = Router(name='admin')
admin_rt.message.middleware(AdminOnlyMiddleware())


@admin_rt.message(Command('report'))
async def report_handler(message: Message):
    await message.answer('Выберите промежуток:', reply_markup=report_kb)


@admin_rt.callback_query(F.data.in_(['day', 'week', 'month', 'all']))
async def report_range_handler(callback_data: CallbackQuery):
    period = callback_data.data
    message = callback_data.message
