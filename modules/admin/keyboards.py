import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp

from utils.helpers import FastConnection


class devicesControlKeyboard:
    @staticmethod
    def main_kb():
        btn1 = InlineKeyboardButton(text='Подключенные устройства')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
        return keyboard

    @staticmethod
    async def active_devices_kb():
        response = await FastConnection(url='https://shiot-production.up.railway.app/devices/active').request()
        if len(response['active_devices']) < 1:
            return None
        btn_list = []
        for device_id in response['active_devices']:
            btn = InlineKeyboardButton(text=f'Устройство: {device_id}', callback_data=f'device,id={device_id}')
            btn_list.append(btn)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[btn_list])
        return keyboard

    @staticmethod
    async def manage_device_kb(device_id: int):
        btn1 = InlineKeyboardButton(text='Отправить команду', callback_data=f'command+{device_id}')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1]])
        return keyboard
