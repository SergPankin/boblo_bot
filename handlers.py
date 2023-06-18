import db

from aiogram import types, Router
from aiogram.filters import Command


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
    arguments = message.text.split()
    if len(arguments) != 3:
        await message.answer("Сорян, не могу понять.\n Нужно ввести что-то типа: /give HrenMorzhoviy 100")
        return
    _, to_user, money = arguments
    if not money.isnumeric():
        await message.answer("Вместо суммы ты ввёл какое-то говно.")
        return
    from_user = message.from_user.username
    if '@' in to_user:
        to_user = to_user.replace('@', '')
    new_balance = db.db_give(from_user, to_user, float(money))
    bablance_for_user = abs(new_balance)
    if new_balance == 'Error':
        print("Что-то в моей работе пошло не так, попробуй-ка позже.")
    elif new_balance == 0:
        await message.answer(f"Ты дал {money} этому, как его... @{to_user}. Теперь вы в расчёте.")
    elif new_balance > 0:
        await message.answer(f"Ты дал {money} этому, как его... @{to_user}. Теперь он должен тебе {bablance_for_user}.")
    elif new_balance < 0:
        await message.answer(f"Ты дал {money} этому, как его... @{to_user}. Теперь ты должен ему {bablance_for_user}.")

@router.message(Command('take'))
async def take_money(message: types.Message):
    arguments = message.text.split()
    if len(arguments) != 3:
        await message.answer("Сорян, не могу понять.\n Нужно ввести что-то типа: /give HrenMorzhoviy 100")
        return
    _, from_user, money = arguments
    if not money.isnumeric():
        await message.answer("Вместо суммы ты ввёл какое-то говно.")
        return
    to_user = message.from_user.username
    if '@' in from_user:
        from_user = from_user.replace('@', '')
    new_balance = db.db_give(from_user, to_user, float(money))
    bablance_for_user = abs(new_balance)
    if new_balance == 'Error':
        print("Что-то в моей работе пошло не так, попробуй-ка позже.")
    elif new_balance == 0:
        await message.answer(f"Ты взял {money} у этого, как его... @{from_user}. Теперь вы в расчёте.")
    elif new_balance > 0:
        await message.answer(f"Ты взял {money} у этого, как его... @{from_user}. Теперь ты должен ему {bablance_for_user}.")
    elif new_balance < 0:
        await message.answer(f"Ты взял {money} у этого, как его... @{from_user}. Теперь он должен тебе {bablance_for_user}.")

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
