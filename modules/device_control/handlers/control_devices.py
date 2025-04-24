from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from dispatcher import bot
from modules.admin.keyboards import devicesControlKeyboard
from modules.device_control.states import ManageDeviceStates
from utils.helpers import filter_data, FastConnection

devices_rt = Router(name='devices')


@devices_rt.message(Command('control'))
async def control_panel(msg: Message):
    keyboard = await devicesControlKeyboard.active_devices_kb()
    text = 'Активные устройства: ' if keyboard else 'Активных устройств не найдено'
    await msg.answer(text, reply_markup=keyboard)


@devices_rt.callback_query(F.data.startswith('device,id='))
async def select_device_h(call: CallbackQuery):
    device_id = filter_data(call.data, 'device,id=')
    await call.bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                     text=f'Устройство: {device_id}',
                                     reply_markup=await devicesControlKeyboard.manage_device_kb(device_id))


@devices_rt.callback_query(F.data.startswith('command'))
async def manage_device_h(call: CallbackQuery, state: FSMContext):
    device_id = filter_data(call.data, 'command+')
    await call.bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                     text=f'Команда для устройства: {device_id}')
    await state.update_data(device_id=device_id, message_id=call.message.message_id)
    await state.set_state(ManageDeviceStates.get_command)


@devices_rt.message(StateFilter(ManageDeviceStates.get_command))
async def send_command(msg: Message, state: FSMContext):
    if 'break' in msg.text:
        await state.clear()
        return
    device_id = (await state.get_data()).get('device_id')
    message_id = (await state.get_data()).get('message_id')
    cmd = msg.text
    connection = FastConnection(
        url=f'https://shiot-production.up.railway.app/devices/control/{device_id}?cmd={cmd}'
    )
    response = await connection.request()
    if not isinstance(response, str):
        response = str(response)
    await msg.answer(text=response)
