import psycopg2
from config import host, user, password, dbname, port, sslmode, target_session_attrs

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
            f"""INSERT INTO transactions (timestamp, from_tp, to_tp, sum, currency_id, comment) VALUES (NOW(), '{from_user_id}', '{to_user_id}', '{money}', '{cur_id}', '{comment}');"""
        )
        print("Added transaction to transactions!")

def db_give(params, cur_id = 1):
    connection = open_db_connection()
    print(params)

    if connection:
        from_user_id = add_and_return_user_id(connection, params.from_user)
        to_user_id = add_and_return_user_id(connection, params.to_user)
        print(f'Это от кого: {from_user_id}')
        print(f'Это кому: {to_user_id}')

        add_transaction(connection, from_user_id, to_user_id, params.money, cur_id, params.comment)

        new_balance = process_pair(connection, from_user_id, to_user_id, params.money, cur_id)
        connection.close()
        print("[INFO] PostgreSQL connection closed")
    else:
        print(SOMETHING_WENT_WRONG_EXC)
        raise Exception(SOMETHING_WENT_WRONG_EXC)

    return new_balance

def request_balance(first_user, second_user, cur_id = 1):
    connection = open_db_connection()
    if connection:
        main_id = add_and_return_user_id(connection, first_user)
        secondary_id = add_and_return_user_id(connection, second_user)
        with connection.cursor() as cursor:
            cursor.execute(
                f"""
                SELECT balance, main_id
                FROM pairs
                WHERE ((main_id = '{main_id}' AND secondary_id = '{secondary_id}') OR (main_id = '{secondary_id}' AND secondary_id = '{main_id}')) AND currency_id = '{cur_id}';
                """
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

    else:
        print("Не удалось установить подключение к БД")
        result = 'Error'

    connection.close()
    print("[INFO] PostgreSQL connection closed")

    return result