import db

from aiogram import types, Router
from aiogram.filters import Command

import src.currency_map as currency_map
from src.balance_params import get_balance_params
from src.default_params import get_default_params
from src.history_message import make_history_message
from src.history_transaction_params import get_history_transaction_params
from src.money_transaction_params import get_money_transaction_params


router = Router()

@router.message(Command('start'))
async def start_command(message: types.Message):
    hello_message = """
    Привет! Я boblo_bot. Помогаю всяким нищим рассчитываться друг с другом за обед и прочее...
    Мои команды:
    /give *** *** (типа когда ты дал денег, потом пишешь кому (логин в телеге) а после сумму (по дефолту в тенге).
    /take *** *** (это когда ты задолжал, первый аргумент - кому, второй - сколько).
    /balance ***  (а это проверить каково состояние баланса между тобой и кем-то, его логин вместо звёздочек).
    """
    await message.answer(text=hello_message)
    await message.delete()

@router.message(Command('give'))
async def give_money(message: types.Message):
    params = await get_money_transaction_params(message)

    new_balance = db.db_give(params)
    bablance_for_user = abs(new_balance)

    cur_name = params.cur_data.cur_name

    if new_balance == 0:
        await message.answer(f"Ты дал {params.money} {cur_name} этому, как его... @{params.to_user}. Теперь вы в расчёте в {cur_name}.")
    elif new_balance > 0:
        await message.answer(f"Ты дал {params.money} {cur_name} этому, как его... @{params.to_user}. Теперь он должен тебе {bablance_for_user} {cur_name}.")
    elif new_balance < 0:
        await message.answer(f"Ты дал {params.money} {cur_name} этому, как его... @{params.to_user}. Теперь ты должен ему {bablance_for_user} {cur_name}.")

@router.message(Command('take'))
async def take_money(message: types.Message):
    params = await get_money_transaction_params(message, True)

    new_balance = db.db_give(params)
    bablance_for_user = abs(new_balance)

    cur_name = params.cur_data.cur_name

    if new_balance == 0:
        await message.answer(f"Ты взял {params.money} {cur_name} у этого, как его... @{params.from_user}. Теперь вы в расчёте в {cur_name}.")
    elif new_balance > 0:
        await message.answer(f"Ты взял {params.money} {cur_name} у этого, как его... @{params.from_user}. Теперь ты должен ему {bablance_for_user} {cur_name}.")
    elif new_balance < 0:
        await message.answer(f"Ты взял {params.money} {cur_name} у этого, как его... @{params.from_user}. Теперь он должен тебе {bablance_for_user} {cur_name}.")

@router.message(Command('balance'))
async def check_balance(message: types.Message):
    params = await get_balance_params(message)
    
    bablance, cur_name = db.request_balance(params)
    bablance_for_user = abs(bablance)

    if bablance == 'Error':
        print("Что-то в моей работе пошло не так, попробуй-ка позже.")
    elif bablance == 0:
        await message.answer(f"Ты с @{params.to_user} в расчёте в {cur_name}. Никто никому ничего не должен...")
    elif bablance > 0:
        await message.answer(f"@{params.to_user} должен тебе {bablance_for_user} {cur_name}. Доставай паяльник...")
    elif bablance < 0:
        await message.answer(f"Ты должен @{params.to_user} {bablance_for_user} {cur_name}. Неплохо бы отдать бабки. Коллекторы уже в пути...")

@router.message(Command('history'))
async def get_history(message: types.Message):
    params = await get_history_transaction_params(message)

    transactions_amount, transaction_list = db.db_get_transactions(params)

    await message.answer(make_history_message(transaction_list, transactions_amount))


SOMETHING_WRONG_EXC = 'Something went WRONG while updating default currency. No users data updated'

# Добавляем новое поле - дефолтная валюта у юзера. По умолчанию ставим тенге
# Делаем массив сокращений валюты для случая, если менять валюту геморно
# Обновляем ручки take/give, balance и history
@router.message(Command('default'))
async def get_history(message: types.Message):
    params = await get_default_params(message)

    is_ok = db.set_default_cur(params)
    if not is_ok:
        await message.answer(SOMETHING_WRONG_EXC)
        raise Exception(SOMETHING_WRONG_EXC)

    await message.answer(f"Default currency of @{params.user} is set to {params.cur_data.cur_name}")

@router.message(Command('alias'))
async def get_history(message: types.Message):
    params = await get_default_params(message)

    currency_aliases_set = currency_map.get_aliases(params)

    msg = f'Aliases for {params.cur_data.cur_name}:\n'
    for alias in currency_aliases_set:
        msg += f"\t{alias}\n"

    await message.answer(msg)
