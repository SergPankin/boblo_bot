from aiogram import types

import src.currency_map as currency_map


class BalanceParams:
    def __init__(
        self,
        from_user = '',
        to_user = '',
        cur_data = '',
    ):
        self.from_user = from_user
        self.to_user = to_user
        self.cur_data = cur_data

    from_user = ''
    to_user = ''
    cur_data = ''


GOVNO_ARGS_EXC = "Сорян, не могу понять.\n Нужно ввести что-то типа: /balance @HrenMorzhoviy [currency_name]"
GOVNO_CURRENCY_EXC = "Вместо валюты ты ввёл какое-то говно."


def check_args_amount(arguments):
    if 2 <= len(arguments) <= 3:
        return True
    return False


def trim_user(user_str):
    if '@' in user_str:
        return user_str.replace('@', '')
    return user_str


async def get_balance_params(message: types.Message):
    arguments = message.text.split()
    if not check_args_amount(arguments):
        await message.answer(GOVNO_ARGS_EXC)
        raise Exception(GOVNO_ARGS_EXC)
    
    result = BalanceParams()
  
    if len(arguments) == 3:
        try:
            result.cur_data = currency_map.get_cur_data(arguments[2])
        except Exception:
            await message.answer(currency_map.make_wrong_currency_message())
            raise

    result.to_user = trim_user(arguments[1])
    result.from_user = trim_user(message.from_user.username)

    return result

