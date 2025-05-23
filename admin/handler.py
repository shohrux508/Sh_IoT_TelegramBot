from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from admin.middlewares import AdminOnlyMiddleware


admin_rt = Router(name='admin')
admin_rt.message.middleware(AdminOnlyMiddleware())


@admin_rt.message(Command('admin'))
async def report_handler(message: Message):
    await message.answer('Вы админ!')


