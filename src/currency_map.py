class CurData:
    def __init__(self, id, name): 
        self.cur_id = id 
        self.cur_name = name
    
    cur_id = ''
    cur_name = ''

KZT_DATA = CurData(1, 'KZT')
KZT_MAP = {
    'kzt',
    't',
    'tn',
    'tng',
    'ten',
    'tenge',
    'т',
    'тг',
    'тнг',
    'тен',
    'тенге',
}

RUB_DATA = CurData(2, 'RUB')
RUB_MAP = {
    'rub',
    'r',
    'ru',
    'ruble',
    'rubles',
    'р',
    'ру',
    'руб',
    'рубл',
    'рубль',
    'рублей',
}

KGS_DATA = CurData(3, 'KGS')
KGS_MAP = {
    'kgs',
    's',
    'sm',
    'som',
    'soms',
    'с',
    'см',
    'сом',
    'сомы',
}

DOLLAR_DATA = CurData(4, 'USD')
DOLLAR_MAP = {
    'usd',
    'd',
    'dlr',
    'dol',
    'doll',
    'dollar',
    'д',
    'доллар',
    '$',
}

EURO_DATA = CurData(5, 'EUR')
EURO_MAP = {
    'eur',
    'e',
    'er',
    'eu',
    'euro',
    'е',
    'евр',
    'евро',
}

ALL_CURRENCIES = [
    (KZT_MAP, KZT_DATA),
    (RUB_MAP, RUB_DATA),
    (KGS_MAP, KGS_DATA),
    (DOLLAR_MAP, DOLLAR_DATA),
    (EURO_MAP, EURO_DATA),
]

CURRENCY_MAP = dict()

for currency_aliases_set, currency_data in ALL_CURRENCIES:
    for currency_alias in currency_aliases_set:
        CURRENCY_MAP[currency_alias.lower()] = currency_data


GOVNO_CURRENCY_EXC = "Вместо валюты ты ввёл какое-то говно."

def get_cur_data(cur_str):
    cur_data = CURRENCY_MAP.get(cur_str)
    if not cur_data:
        raise Exception(GOVNO_CURRENCY_EXC)
    
    return cur_data


def make_wrong_currency_message():
    msg = GOVNO_CURRENCY_EXC
    msg += f'\nДоступные сейчас валюты: \n'
    for _, currency_data in ALL_CURRENCIES:
        msg += f'{currency_data.cur_name}\n'
    
    #for key, value in CURRENCY_MAP.items():
    #    print(f"{key}: {value.cur_name}")

    return msg
