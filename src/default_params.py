from aiogram import types

import src.currency_map as currency_map

class DefaultParams:
    user = ''
    cur_data = '' #[cur_id, cur_name]


GOVNO_ARGS_EXC = "Сорян, не могу понять.\n Нужно ввести что-то типа: /default RUB"
GOVNO_CURRENCY_EXC = "Вместо валюты ты ввёл какое-то говно."


def check_args_amount(arguments):
    if len(arguments) == 2:
        return True
    return False


def trim_user(user_str):
    if '@' in user_str:
        return user_str.replace('@', '')
    return user_str


async def get_default_params(message: types.Message):
    arguments = message.text.split()
    if not check_args_amount(arguments):
        await message.answer(GOVNO_ARGS_EXC)
        raise Exception(GOVNO_ARGS_EXC)
    
    result = DefaultParams()
  
    try:
        result.cur_data = currency_map.get_cur_data(arguments[1])
    except:
        await message.answer(currency_map.make_wrong_currency_message())
        raise
    
    result.user = trim_user(message.from_user.username)

    return result
