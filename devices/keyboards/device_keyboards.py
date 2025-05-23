from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Мои устройства', callback_data='my-devices')],
        [InlineKeyboardButton(text='Добавить устройство', callback_data='add-device')],
        [InlineKeyboardButton(text='Помощь', callback_data='devices-help')]
    ])


def manage_device_kb(device_id: int, device_type: str, status: bool | int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Включить', callback_data=f'control-device,{device_id},{device_type},turn_on')],
        [InlineKeyboardButton(text='Выключить', callback_data=f'control-device,{device_id},{device_type},turn_off')],
        [InlineKeyboardButton(text='Настроить таймер', callback_data=f'control-device,{device_id},{device_type},set_timer')],
        [InlineKeyboardButton(text='Выключить таймер', callback_data=f'control-device,{device_id},{device_type},clear_timer')],
    ])
