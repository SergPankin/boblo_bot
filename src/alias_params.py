from aiogram import types

import src.currency_map as currency_map

class AliasParams:
    cur_data = '' #[cur_id, cur_name]


GOVNO_ARGS_EXC = "Сорян, не могу понять.\n Нужно ввести что-то типа: /aliases EUR"
GOVNO_CURRENCY_EXC = "Вместо валюты ты ввёл какое-то говно."


def check_args_amount(arguments):
    if len(arguments) == 2:
        return True
    return False


async def get_alias_params(message: types.Message):
    arguments = message.text.split()
    if not check_args_amount(arguments):
        await message.answer(GOVNO_ARGS_EXC)
        raise Exception(GOVNO_ARGS_EXC)
    
    result = AliasParams()
  
    try:
        result.cur_data = currency_map.get_cur_data(arguments[1])
    except:
        await message.answer(currency_map.make_wrong_currency_message())
        raise

    return result
