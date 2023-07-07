from aiogram import types

from src.currency_map import CURRENCY_MAP

class DefaultParams:
    user = ''
    cur_data = '' #[cur_id, cur_name]


GOVNO_ARGS_EXC = "Сорян, не могу понять.\n Нужно ввести что-то типа: /default RUB"
GOVNO_CURRENCY_EXC = "Вместо валюты ты ввёл какое-то говно."


def check_args_amount(arguments):
    if len(arguments) == 1:
        return True
    return False


def get_cur_data(cur_str):
    cur_data = CURRENCY_MAP.get(cur_str)
    if not cur_data:
        raise Exception(GOVNO_CURRENCY_EXC)
    
    return cur_data


def trim_user(user_str):
    if '@' in user_str:
        return user_str.replace('@', '')
    return user_str


def make_wrong_currency_message():
    msg = GOVNO_CURRENCY_EXC
    msg += f'Доступные сейчас валюты: \n'
    for currency_data in CURRENCY_MAP:
        msg += f'{currency_data.cur_name}\n'

    return msg


async def get_default_params(message: types.Message):
    arguments = message.text.split()
    if not check_args_amount(arguments):
        await message.answer(GOVNO_ARGS_EXC)
        raise Exception(GOVNO_ARGS_EXC)
    
    result = DefaultParams()
  
    try:
        result.cur_data = get_cur_data(arguments[1])
    except:
        await message.answer(make_wrong_currency_message())
        raise
    
    result.user = trim_user(message.from_user.username)

    return result
