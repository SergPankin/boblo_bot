import db

from aiogram import types, Router
from aiogram.filters import Command

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

    if new_balance == 0:
        await message.answer(f"Ты дал {params.money} этому, как его... @{params.to_user}. Теперь вы в расчёте.")
    elif new_balance > 0:
        await message.answer(f"Ты дал {params.money} этому, как его... @{params.to_user}. Теперь он должен тебе {bablance_for_user}.")
    elif new_balance < 0:
        await message.answer(f"Ты дал {params.money} этому, как его... @{params.to_user}. Теперь ты должен ему {bablance_for_user}.")

@router.message(Command('take'))
async def take_money(message: types.Message):
    params = await get_money_transaction_params(message, True)

    new_balance = db.db_give(params)
    bablance_for_user = abs(new_balance)

    if new_balance == 0:
        await message.answer(f"Ты взял {params.money} у этого, как его... @{params.from_user}. Теперь вы в расчёте.")
    elif new_balance > 0:
        await message.answer(f"Ты взял {params.money} у этого, как его... @{params.from_user}. Теперь ты должен ему {bablance_for_user}.")
    elif new_balance < 0:
        await message.answer(f"Ты взял {params.money} у этого, как его... @{params.from_user}. Теперь он должен тебе {bablance_for_user}.")

@router.message(Command('balance'))
async def check_balance(message: types.Message):
    arguments = message.text.split()
    if len(arguments) != 2:
        await message.answer("Сорян, не могу понять.\n Нужно ввести что-то типа: /balance HrenMorzhoviy")
        return
    first_user = message.from_user.username
    second_user = arguments[1]
    if '@' in second_user:
        second_user = second_user.replace('@', '')
    bablance = db.request_balance(first_user, second_user)
    bablance_for_user = abs(bablance)
    if bablance == 'Error':
        print("Что-то в моей работе пошло не так, попробуй-ка позже.")
    elif bablance == 0:
        await message.answer(f"Ты с @{second_user} в расчёте. Никто никому ничего не должен...")
    elif bablance > 0:
        await message.answer(f"@{second_user} должен тебе {bablance_for_user}. Доставай паяльник...")
    elif bablance < 0:
        await message.answer(f"Ты должен @{second_user} {bablance_for_user}. Неплохо бы отдать бабки. Коллекторы уже в пути...")
