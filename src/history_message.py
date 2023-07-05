import datetime 

dayname_dict = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday",
}


def make_date(time):
    return f"{time.isoformat()} ({dayname_dict[time.weekday()]})"


def format_history_message(item, current_using_timestamp):
    user1 = f'@{item.from_user}'
    user2 = f'@{item.to_user}'
    sum = str(item.sum)
    if item.is_reversed_as_for_from_user:
        user1, user2 = user2, user1
        sum = f"-{sum}"
    
    formatted_msg = ''
    if (current_using_timestamp != item.timestamp):
        formatted_msg += f"\n{make_date(item.timestamp)}:\n"
        current_using_timestamp = item.timestamp
    
    formatted_msg += user1 + " ===>>> " + user2 + f": {sum} {item.currency_name}\n"

    if not item.comment == '':
        formatted_msg += f"Comment: {item.comment}\n"

    return formatted_msg, current_using_timestamp


def make_history_message(transaction_list, transactions_amount):
    cur_tp = datetime.date.min
    msg = f"In total {len(transaction_list)}/{transactions_amount} transactions printed\n"
    for transaction_item in transaction_list:
        new_msg, cur_tp = format_history_message(transaction_item, cur_tp)
        msg += new_msg

    return msg
