from aiogram import types

import re


import src.currency_map as currency_map


class MoneyTransactionParams:
    from_user = ''
    to_user = ''
    money = ''
    cur_data = ''
    comment = ''


GOVNO_ARGS_EXC = "Сорян, не могу понять.\n Нужно ввести что-то типа: /give @HrenMorzhoviy 100 [comment]"
GOVNO_MONEY_EXC = "Вместо суммы ты ввёл какое-то говно."
GOVNO_CURRENCY_EXC = "Вместо валюты ты ввёл какое-то говно."


def check_args_amount(arguments):
    if 3 <= len(arguments) <= 4:
        return True
    return False


def make_money_from_string(money_str):
    number = re.search('\d+', money_str)
    if not number:
        raise ValueError(GOVNO_MONEY_EXC)

    money = float(number.group())
    currency_str = money_str[len(number.group()):]
    if len(currency_str) == 0:
        return (money, '')

    cur_data = currency_map.get_cur_data(currency_str)
    if not cur_data:
        raise Exception(GOVNO_CURRENCY_EXC)
        
    return (money, cur_data)

def trim_user(user_str):
    if '@' in user_str:
        return user_str.replace('@', '')
    return user_str


def get_comment(arguments):
    if len(arguments) == 3:
        return ''
    return ' '.join(arguments[3:])


def reverse_users(params):
    params.to_user, params.from_user = params.from_user, params.to_user


async def get_money_transaction_params(message: types.Message, should_reverse_users=False):
    arguments = message.text.split()
    if not check_args_amount(arguments):
        await message.answer(GOVNO_ARGS_EXC)
        raise Exception(GOVNO_ARGS_EXC)
    
    result = MoneyTransactionParams()
  
    try:
        result.money, result.cur_data = make_money_from_string(arguments[2])
    except ValueError:
        await message.answer(GOVNO_ARGS_EXC)
        raise
    except Exception:
        await message.answer(currency_map.make_wrong_currency_message())
        raise

    result.to_user = trim_user(arguments[1])
    result.from_user = trim_user(message.from_user.username)

    if (should_reverse_users):
        reverse_users(result)

    result.comment = get_comment(arguments)

    return result
