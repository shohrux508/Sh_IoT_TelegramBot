import asyncio

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import aiohttp

from utils.helpers import FastConnection


class devicesControlKeyboard:
    @staticmethod
    def main_kb():
        btn1 = InlineKeyboardButton(text='Мои устройства', callback_data='my-devices')
        btn2 = InlineKeyboardButton(text='Добавить устройство', callback_data='add-device')
        btn3 = InlineKeyboardButton(text='Помощь', callback_data='devices-help')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3]])
        return keyboard

    @staticmethod
    async def active_devices_kb(active_devices):
        if len(response['active_devices']) < 1:
            print('Устройства не подключены!')
            # return None
        print(response['active_devices'])
        socket_state = 1 if '1' in response['active_devices'] or 1 in response['active_devices'] else 0
        btn_socket1 = InlineKeyboardButton(text='Розетка🟢', callback_data='devices-socket,1')
        btn_socket0 = InlineKeyboardButton(text='Розетка⚫', callback_data='pass')
        btn1 = btn_socket1 if socket_state == 1 else btn_socket0
        btn2 = InlineKeyboardButton(text='Водонагреватель', callback_data='devices-water_heater,2')
        btn3 = InlineKeyboardButton(text='Вентиляция', callback_data='devices-ventilation,3')
        active_btn_list = []
        for device_id in response['active_devices']:
            btn = InlineKeyboardButton(text=f'Устройство: {device_id}', callback_data=f'device,id={device_id}')
            active_btn_list.append(btn)
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1], active_btn_list])
        return keyboard

    @staticmethod
    async def manage_device_kb(device_id: int, device_type: str, status: bool | int):
        btn1 = InlineKeyboardButton(text='Включить', callback_data=f'control-device,{device_id},{device_type},turn_on')
        btn2 = InlineKeyboardButton(text='Выключить',
                                    callback_data=f'control-device,{device_id},{device_type},turn_off')
        btn3 = InlineKeyboardButton(text='Настроить таймер',
                                    callback_data=f'control-device,{device_id},{device_type},set_timer')
        btn4 = InlineKeyboardButton(text='Выключить таймер',
                                    callback_data=f'control-device,{device_id},{device_type},clear_timer')
        btn = btn2 if status else btn1
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn], [btn3], [btn4]])
        return keyboard

