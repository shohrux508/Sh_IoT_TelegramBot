import asyncio
import json

from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from modules.admin.keyboards import devicesControlKeyboard
from modules.device_control.control_time import handle_time_input, time_kb
from modules.device_control.states import SocketControlStates
from utils.helpers import filter_data, FastConnection

devices_rt = Router(name='devices')

local_url = 'http://127.0.0.1:8000'
pub_url = f'https://shiot-production.up.railway.app'
url = pub_url


@devices_rt.message(Command('start'))
async def start_h(msg: Message):
    await msg.answer('🏠', reply_markup=devicesControlKeyboard.main_kb())


@devices_rt.callback_query(F.data.startswith('my-devices'))
async def control_panel(call: CallbackQuery):
    active_devices = await FastConnection(url='https://shiot-production.up.railway.app/devices/active').request()

    keyboard = await devicesControlKeyboard.active_devices_kb(active_devices=)
    text = 'Активные устройства: ' if keyboard else 'Активных устройств не найдено'
    count = 0
    while count < 30:
        await asyncio.sleep(1)
        await call.bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                         text=f"{text}\n{30 - count}",
                                         reply_markup=keyboard)
        count += 1
    await call.message.delete()


@devices_rt.callback_query(F.data.startswith('devices-'))
async def select_device_h(call: CallbackQuery):
    device_type, device_id = (filter_data(call.data, 'devices-')).split(',')
    await call.bot.edit_message_text(chat_id=call.from_user.id, message_id=call.message.message_id,
                                     text=f'Управление устройством: {device_type}',
                                     reply_markup=await devicesControlKeyboard.manage_device_kb(device_id=device_id,
                                                                                                device_type=device_type,
                                                                                                status=True))


@devices_rt.callback_query(F.data.startswith('control-device,'))
async def control_device_h(call: CallbackQuery):
    device_id, device_type, action = (filter_data(call.data, 'control-device,')).split(',')
    s_state = 1 if action == 'turn_on' else 0

    connection = FastConnection(url=f"{url}/devices/control/{device_id}")
    data = {'device_type': device_type}
    if action == 'set_timer':
        await call.message.answer(text='Задайте время запуска. **:**',
                                  reply_markup=await time_kb(device_id=device_id, device_type=device_type))
        return
    elif action == 'clear_timer':
        pass
    else:
        data["state"] = s_state
    print(s_state)
    response = await connection.request(method='POST', data=data)
    if not isinstance(response, str):
        response = str(response)
    await call.answer(response, show_alert=True)


@devices_rt.callback_query(F.data.startswith('time'))
async def time_h(call: CallbackQuery, state: FSMContext):
    response = await handle_time_input(call, state)
    if response:
        time_start = response[0]
        time_stop = response[1]
        device_id = response[2]
        device_type = response[3]
        connection = FastConnection(url=f"{url}/devices/control/{device_id}")
        context = {
            "device_type": device_type,
            "state": True,
            "start_time": time_start,
            "stop_time": time_stop
        }
        response = await connection.request(data=context, method='POST')
        if not isinstance(response, str):
            response = str(response)
        await call.answer(response, show_alert=True)
