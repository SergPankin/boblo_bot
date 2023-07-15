from aiogram import types

import src.currency_map as currency_map

class HistoryTransactionParams:
    def __init__(
        self,
        from_user = '',
        to_user = '',
        history_length = '',
        cur_data = '',
    ):
        self.from_user = from_user
        self.to_user = to_user
        self.history_length = history_length
        self.cur_data = cur_data

    from_user = ''
    to_user = ''
    history_length = ''
    cur_data = ''


GOVNO_ARGS_EXC = "Сорян, не могу понять.\n Нужно ввести что-то типа: /history @HrenMorzhoviy 10 [currency_name]"
GOVNO_HISTORY_EXC = "Вместо количества транзакций ты ввёл какое-то говно."
GOVNO_CURRENCY_EXC = "Вместо валюты ты ввёл какое-то говно."


def check_args_amount(arguments):
    if 3 <= len(arguments) <= 4:
        return True
    return False


def check_history_length(len_str):
    if len_str == '*':
        return True
    if len_str.isnumeric() and int(len_str) > 0:
        return True
    return False


def trim_user(user_str):
    if '@' in user_str:
        return user_str.replace('@', '')
    return user_str


def reverse_users(params):
    params.to_user, params.from_user = params.from_user, params.to_user


async def get_history_transaction_params(message: types.Message):
    arguments = message.text.split()
    if not check_args_amount(arguments):
        await message.answer(GOVNO_ARGS_EXC)
        raise Exception(GOVNO_ARGS_EXC)
    
    result = HistoryTransactionParams()
  
    result.to_user = trim_user(arguments[1])
    result.from_user = trim_user(message.from_user.username)

    history_length = arguments[2]
    if not check_history_length(history_length):
        await message.answer(GOVNO_HISTORY_EXC)
        raise Exception(GOVNO_HISTORY_EXC)
    
    result.history_length = 0 if history_length == '*' else int(history_length)

    if len(arguments) == 4:
        try:
            result.cur_data = currency_map.get_cur_data(arguments[3])
        except Exception:
            await message.answer(currency_map.make_wrong_currency_message())
            raise

    return result
