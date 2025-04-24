from aiogram.filters.state import StatesGroup, State

class ManageDeviceStates(StatesGroup):
    get_command = State()
