import psycopg2
from config import host, user, password, dbname, port, sslmode, target_session_attrs

from src.currency_map import CurData 

SOMETHING_WENT_WRONG_EXC = "Что-то в моей работе пошло не так, попробуй-ка позже."


def open_db_connection():
    try:
        connection = psycopg2.connect(
            host=host,
            user=user,
            password=password,
            database=dbname,
            port=port,
            sslmode=sslmode,
            target_session_attrs=target_session_attrs,
        )
        connection.autocommit = True
        return connection

    except Exception as ex:
        print("[INFO] Error while working with PostgreSQL", ex)

def add_and_return_user_id(connection, user_login):
    with connection.cursor() as cursor:
        cursor.execute(
            f"SELECT user_id FROM users WHERE tg_login = '{user_login}';"
        )
        user_record = cursor.fetchone()
    if not user_record:
        with connection.cursor() as cursor:
            cursor.execute(
                f"""INSERT INTO users (tg_login) VALUES ('{user_login}');"""
                f"SELECT user_id FROM users WHERE tg_login = '{user_login}';"
            )
            user_id = cursor.fetchone()[0]
    else:
        user_id = user_record[0]
    return user_id

def process_pair(connection, from_user_id, to_user_id, money, cur_id):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""
            SELECT pair_id, main_id, secondary_id, balance, currency_id
            FROM pairs
            WHERE ((main_id = '{from_user_id}' AND secondary_id = '{to_user_id}') OR (main_id = '{to_user_id}' AND secondary_id = '{from_user_id}')) AND currency_id = '{cur_id}';
            """
        )
        current_pair = cursor.fetchone()
        if current_pair:
            old_balance = float(current_pair[3])
            if from_user_id == int(current_pair[1]):
                new_balance = old_balance + money
                result = float(new_balance)
            elif from_user_id == int(current_pair[2]):
                new_balance = old_balance - money
                result = float(new_balance) * (-1)
            cursor.execute(
                f"""
                UPDATE pairs
                    SET balance = '{new_balance}'
                    WHERE pair_id = '{current_pair[0]}'
                """
            )
        else:
            result = money
            cursor.execute(
                f"""
                INSERT INTO pairs (main_id, secondary_id, balance, currency_id) 
                VALUES ('{from_user_id}', '{to_user_id}', '{money}', '{cur_id}')
                """
            )
    return result

def add_transaction(connection, from_user_id, to_user_id, money, cur_id, comment):
    with connection.cursor() as cursor:
        cursor.execute(
            f"""INSERT INTO transactions (
                    timestamp,
                    from_tp,
                    to_tp,
                    sum,
                    currency_id,
                    comment
                ) VALUES (
                    NOW(),
                    '{from_user_id}',
                    '{to_user_id}',
                    '{money}',
                    '{cur_id}',
                    '{comment}'
                );
            """
        )
        print("Added transaction to transactions!")


GET_DEFAULT_CURRENCY = """
    SELECT default_cur
    FROM users
    WHERE user_id = {user_id};
"""

GET_CURRENCY_NAME = """
    SELECT
        cur_name
    FROM currencies
    WHERE cur_id = {cur_id};
"""

def get_default_currency(connection, user_id):
    with connection.cursor() as cursor:
        cursor.execute(
            GET_DEFAULT_CURRENCY.format(
                user_id=user_id,
            )
        )
        cur_id = cursor.fetchone()[0]
        cursor.execute(
            GET_CURRENCY_NAME.format(
                cur_id=cur_id
            )
        )
        cur_name = cursor.fetchone()[0]
        return CurData(cur_id, cur_name)


def db_give(params):
    connection = open_db_connection()

    if connection:
        from_user_id = add_and_return_user_id(connection, params.from_user)
        to_user_id = add_and_return_user_id(connection, params.to_user)
        print(f'Это от кого: {from_user_id}')
        print(f'Это кому: {to_user_id}')

        if params.cur_data == '':
            default_cur_user_id = add_and_return_user_id(connection, params.def_cur_user)
            params.cur_data = get_default_currency(connection, default_cur_user_id)

        add_transaction(connection, from_user_id, to_user_id, params.money, params.cur_data.cur_id, params.comment)

        new_balance = process_pair(connection, from_user_id, to_user_id, params.money, params.cur_data.cur_id)
        connection.close()
        print("[INFO] PostgreSQL connection closed")
    else:
        print(SOMETHING_WENT_WRONG_EXC)
        raise Exception(SOMETHING_WENT_WRONG_EXC)

    return new_balance

GET_BALANCE = """
    SELECT
        balance,
        main_id
    FROM pairs
    WHERE (
        (main_id = '{main_id}' AND secondary_id = '{secondary_id}') 
       OR 
        (main_id = '{secondary_id}' AND secondary_id = '{main_id}')
        )
      AND currency_id = '{cur_id}';
"""

def request_balance(params):
    connection = open_db_connection()
    if connection:
        main_id = add_and_return_user_id(connection, params.from_user)
        secondary_id = add_and_return_user_id(connection, params.to_user)

        if params.cur_data == '':
            params.cur_data = get_default_currency(connection, main_id)

        with connection.cursor() as cursor:
            cursor.execute(
                GET_BALANCE.format(
                    main_id=main_id,
                    secondary_id=secondary_id,
                    cur_id=params.cur_data.cur_id,
                )
            )
            current_pair = cursor.fetchone()
            if current_pair:
                balance = float(current_pair[0])
                pair_main_id = current_pair[1]
                if main_id != pair_main_id:
                    result = balance * (-1)
                else:
                    result = balance
            else:
                result = 0.00

        connection.close()
    else:
        print("Не удалось установить подключение к БД")
        result = 'Error'

    print("[INFO] PostgreSQL connection closed")

    return result, params.cur_data.cur_name


GET_TRANSACTIONS = """
    SELECT
        timestamp,
        from_tp,
        to_tp,
        sum,
        currency_id,
        comment
    FROM transactions
    WHERE (
        (from_tp = {from_user} AND to_tp = {to_user})
       OR
        (from_tp = {to_user} AND to_tp = {from_user})
        )
      AND currency_id = {cur_id}
    ORDER BY timestamp DESC
    LIMIT {limit};
"""

GET_ALL_TRANSACTIONS = """
    SELECT
        timestamp,
        from_tp,
        to_tp,
        sum,
        currency_id,
        comment
    FROM transactions
    WHERE (
        (from_tp = {from_user} AND to_tp = {to_user})
       OR
        (from_tp = {to_user} AND to_tp = {from_user})
        )
      AND currency_id = {cur_id}
    ORDER BY timestamp DESC;
"""

GET_TRANSACTIONS_AMOUNT = """
    SELECT
        COUNT(*)
    FROM transactions
    WHERE (
        (from_tp = {from_user} AND to_tp = {to_user})
       OR
        (from_tp = {to_user} AND to_tp = {from_user})
        )
      AND currency_id = {cur_id};
"""

def get_transactions(connection, params, from_user_id, to_user_id):
    with connection.cursor() as cursor:
        if params.history_length:
            cursor.execute(
                GET_TRANSACTIONS.format(
                    from_user=from_user_id,
                    to_user=to_user_id,
                    cur_id=params.cur_data.cur_id,
                    limit=params.history_length
                )
            )
        else:
            cursor.execute(
                GET_ALL_TRANSACTIONS.format(
                    from_user=from_user_id,
                    to_user=to_user_id,
                    cur_id=params.cur_data.cur_id
                )
            )
        history_list = cursor.fetchall()

        cursor.execute(
            GET_TRANSACTIONS_AMOUNT.format(
                    from_user=from_user_id,
                    to_user=to_user_id,
                    cur_id=params.cur_data.cur_id,
                )
        )
        history_amount = cursor.fetchone()[0]
    return history_amount, history_list


def process_timestamp(time):
    return time.date()


class HistoryListItem:
    timestamp='',
    from_user='',
    to_user='',
    sum='',
    currency_name='',
    comment=''
    is_reversed_as_for_from_user=False


#timestamp 0
#from_tp 1
#to_tp 2
#sum 3
#currency_id 4
#comment 5
def process_history_item(item, params, from_user_id):
    result = HistoryListItem()
    result.timestamp = process_timestamp(item[0]) #timestamp

    result.from_user = params.from_user
    result.to_user = params.to_user
    if item[1] != from_user_id: #from_user
        result.is_reversed_as_for_from_user = True

    result.sum = item[3] #sum

    result.currency_name = params.cur_data.cur_name
    result.comment = item[5] #comment

    return result

def db_get_transactions(params):
    connection = open_db_connection()

    if connection:
        from_user_id = add_and_return_user_id(connection, params.from_user)
        to_user_id = add_and_return_user_id(connection, params.to_user)
        print(f'Это от кого: {from_user_id}')
        print(f'Это кому: {to_user_id}')

        if params.cur_data == '':
            params.cur_data = get_default_currency(connection, from_user_id)

        history_amount, history_list = get_transactions(connection, params, from_user_id, to_user_id)

        list_processed_history = []
        for history_item in reversed(history_list):
            processed_history_item = process_history_item(history_item, params, from_user_id)
            list_processed_history.append(processed_history_item)

        connection.close()
        print("[INFO] PostgreSQL connection closed")
    else:
        print(SOMETHING_WENT_WRONG_EXC)
        raise Exception(SOMETHING_WENT_WRONG_EXC)

    return history_amount, list_processed_history


UPDATE_DEFAULT_CURRENCY = """
    WITH upd AS (
        UPDATE users
        SET
            default_cur = {cur}
        WHERE user_id = {user_id}
        RETURNING 1
    )
    SELECT COUNT(*) from upd;
"""


def set_default_cur(params):
    is_successful = False
    connection = open_db_connection()

    if connection:
        user_id = add_and_return_user_id(connection, params.user)
        print(f'Кому проставляем дефолтную валюту: {user_id}')

        with connection.cursor() as cursor:
            cursor.execute(
                UPDATE_DEFAULT_CURRENCY.format(
                    user_id=user_id,
                    cur=params.cur_data.cur_id,
                )
            )
            users_updated_amount = cursor.fetchone()[0]
            is_successful = users_updated_amount != 0

        connection.close()
        print("[INFO] PostgreSQL connection closed")
    else:
        print(SOMETHING_WENT_WRONG_EXC)
        raise Exception(SOMETHING_WENT_WRONG_EXC)

    return is_successful
