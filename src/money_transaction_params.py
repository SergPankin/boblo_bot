from aiogram import types


class MoneyTransactionParams:
    from_user = ''
    to_user = ''
    money = ''
    comment = ''


GOVNO_ARGS_EXC = "Сорян, не могу понять.\n Нужно ввести что-то типа: /give @HrenMorzhoviy 100 [comment]"
GOVNO_MONEY_EXC = "Вместо суммы ты ввёл какое-то говно."


def check_args_amount(arguments):
    if 3 <= len(arguments):
        return True
    return False


def check_money_string(str_money):
    if str_money.isnumeric():
        return True
    return False

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
  
    money = arguments[2]
    if not check_money_string(money):
        await message.answer(GOVNO_MONEY_EXC)
        raise Exception(GOVNO_MONEY_EXC)
    
    result.money = float(money)
    
    result.to_user = trim_user(arguments[1])
    result.from_user = trim_user(message.from_user.username)

    if (should_reverse_users):
        reverse_users(result)

    result.comment = get_comment(arguments)

    return result
