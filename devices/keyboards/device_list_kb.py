from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from devices.services.device_service import DeviceService


async def devices_kb() -> InlineKeyboardMarkup | None:
    devices = await DeviceService.get_devices()
    if not devices:
        return None

    buttons = []
    for device in devices:
        status = await DeviceService.get_device_status(device['id'])
        symbol = '🟢' if status else '⚫'
        btn = InlineKeyboardButton(
            text=f"{device['name']}:{symbol}",
            callback_data=f"devices-{device['name']},{device['id']}"
        )
        buttons.append(btn)

    inline = [buttons[i:i + 2] for i in range(0, len(buttons), 2)]
    return InlineKeyboardMarkup(inline_keyboard=inline)
