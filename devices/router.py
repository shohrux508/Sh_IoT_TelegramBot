import asyncio
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from devices.api.device_api import DeviceAPI
from devices.keyboards.device_keyboards import main_kb, manage_device_kb
from devices.keyboards.device_list_kb import devices_kb
from devices.keyboards.time_keyboard import time_kb
from devices.services.timer_service import handle_time_input

from utils.helpers import filter_data

devices_rt = Router(name="devices")


@devices_rt.message(Command("start"))
async def start_h(msg: Message):
    await msg.answer("🏠", reply_markup=main_kb())


@devices_rt.callback_query(F.data == "my-devices")
async def control_panel(call: CallbackQuery):
    count = 0
    while count < 30:
        keyboard = await devices_kb()
        text = "Все устройства:" if keyboard else "Устройств не найдено"

        await asyncio.sleep(3)
        await call.bot.edit_message_text(
            chat_id=call.from_user.id,
            message_id=call.message.message_id,
            text=f"{text}\n{30 - count}",
            reply_markup=keyboard
        )
        count += 3
    await call.message.delete()


@devices_rt.callback_query(F.data.startswith("devices-"))
async def select_device_h(call: CallbackQuery):
    try:
        device_type, device_id = filter_data(call.data, "devices-").split(",")
        await call.message.answer(
            text=f"Управление устройством: {device_type}",
            reply_markup=manage_device_kb(device_id=int(device_id), device_type=device_type, status=True)
        )
    except Exception as e:
        await call.answer("Ошибка выбора устройства", show_alert=True)


@devices_rt.callback_query(F.data.startswith("control-device,"))
async def control_device_h(call: CallbackQuery):
    try:
        device_id, device_type, action = filter_data(call.data, "control-device,").split(",")
    except ValueError:
        await call.answer("Ошибка в данных", show_alert=True)
        return

    if action == "set_timer":
        await call.message.answer(
            text="Задайте время запуска. **:**",
            reply_markup=await time_kb(device_id=int(device_id), device_type=device_type)
        )
        return

    if action == "clear_timer":
        response = await DeviceAPI.clear_timer(device_id=int(device_id))
        await call.answer(str(response), show_alert=True)
        return
    if action == 'get-status':
        response = await DeviceAPI.get_status(device_id=int(device_id))

    # Включение/выключение устройства
    state = 1 if action == "turn_on" else 0
    response = await DeviceAPI.send_state(device_id=int(device_id), state=state)
    await call.answer(str(response), show_alert=True)


@devices_rt.callback_query(F.data.startswith("time"))
async def time_h(call: CallbackQuery, state: FSMContext):
    result = await handle_time_input(call, state)
    if not result:
        return

    start, stop, device_id, device_type = result

    response = await DeviceAPI.set_timer(device_id=int(device_id), start=start, stop=stop)
    await call.answer(str(response), show_alert=True)
