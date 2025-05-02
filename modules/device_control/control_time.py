from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from datetime import datetime


def highlight_cursor(text: str, cursor: int) -> str:
    if 0 <= cursor < len(text):
        return text[:cursor] + '\u0332' + text[cursor] + text[cursor + 1:]
    return text


async def time_kb(device_id: int, device_type: str, cursor: int = 0) -> InlineKeyboardMarkup:
    digits = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    keyboard = [
        [InlineKeyboardButton(text=str(n), callback_data=f'time,{n},{cursor},{device_id},{device_type}') for n in row]
        for row in digits
    ]
    keyboard.append([
        InlineKeyboardButton(text='0', callback_data=f'time,0,{cursor},{device_id},{device_type}'),
        InlineKeyboardButton(text='🔙', callback_data=f'time,*,{cursor},{device_id},{device_type}'),
        InlineKeyboardButton(text='✅', callback_data=f'time,submit,{cursor},{device_id},{device_type}')
    ])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def filter_data(source: str, prefix: str) -> str:
    return source.replace(prefix, '').strip()


async def handle_time_input(call: CallbackQuery, state: FSMContext):
    value, cursor, device_id, device_type = (filter_data(call.data, 'time,')).split(',')
    cursor = int(cursor)

    data = await state.get_data()
    time_string = data.get("edit_time", "00:00–00:00")
    time_list = list(time_string)

    if value == '*':
        if cursor >= len(time_list):
            cursor = len(time_list) - 1

        while cursor > 0 and time_list[cursor] in {':', '–'}:
            cursor -= 1
        time_list[cursor] = '0'
        next_cursor = max(0, cursor - 1)
        if time_list[next_cursor] in {':', '–'}:
            next_cursor = max(0, next_cursor - 1)

    elif value == 'submit':

        start = ''.join(time_list[0:5])
        stop = ''.join(time_list[6:11])
        try:
            fmt = "%H:%M"
            t1 = datetime.strptime(start, fmt)
            t2 = datetime.strptime(stop, fmt)
            if t1 >= t2:
                await call.answer("Время выключения должно быть позже включения", show_alert=True)
                return
        except Exception:
            await call.answer("Ошибка формата времени", show_alert=True)
            return

        await call.message.edit_text(f"Время включения: {start}\nВремя выключения: {stop}")

        return start, stop, device_id, device_type

    else:
        if cursor >= len(time_list):
            cursor = len(time_list) - 1

        if time_list[cursor] in {':', '–'}:
            cursor += 1
        time_list[cursor] = value
        next_cursor = cursor + 1
        while next_cursor < len(time_list) and time_list[next_cursor] in {':', '–'}:
            next_cursor += 1
        next_cursor = min(len(time_list), next_cursor)

    new_time_string = ''.join(time_list)
    await state.update_data(edit_time=new_time_string)
    highlighted = highlight_cursor(new_time_string, next_cursor)
    try:
        await call.message.edit_text(
            text=f"Установите время:\n{highlighted}",
            reply_markup=await time_kb(cursor=next_cursor, device_id=int(device_id), device_type=device_type)
        )
    except:
        pass
