from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


class devicesControlKeyboard:
    @staticmethod
    def main_kb():
        btn1 = InlineKeyboardButton(text='Мои устройства', callback_data='my-devices')
        btn2 = InlineKeyboardButton(text='Добавить устройство', callback_data='add-device')
        btn3 = InlineKeyboardButton(text='Помощь', callback_data='devices-help')
        keyboard = InlineKeyboardMarkup(inline_keyboard=[[btn1], [btn2], [btn3]])
        return keyboard

    @staticmethod
    async def devices_kb(dlist: list):
        if len(dlist) < 1:
            print('Пусто!')
            return None
        btn_list = []
        for device in dlist:
            name = device['name']
            pk = device['id']
            status = '🟢' if True else '⚫'
            btn = InlineKeyboardButton(text=f"{name}:{status}", callback_data=f'devices-{name},{pk}')
            btn_list.append(btn)
        inline_keyboard = [btn_list[i:i + 2] for i in range(0, len(btn_list), 2)]
        keyboard = InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
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
