class CurData:
    cur_id = ''
    cur_name = ''

KZT_DATA = CurData(1, 'KZT')
KZT_MAP = set(
    'kzt',
    'т'
    'тенге',
)

RUB_DATA = CurData(2, 'RUB')
RUB_MAP = set(
    'rub',
    'р',
    'руб',
    'рубль',
    'рублей',
)

KGS_DATA = CurData(3, 'KGS')
KGS_MAP = set(
    'kgs',
    's',
    'som',
    'с',
    'сом',
    'сомы'
)

KZT_DATA = CurData(4, 'USD')
DOLLAR_MAP = set(
    'usd',
    'd',
    'dollar',
    'д',
    'доллар',
    '$',
)

EURO_DATA = CurData(5, 'EUR')
EURO_MAP = set(
    'eur',
    'e',
    'eu',
    'euro',
    'е',
    'евр',
    'евро',
)

ALL_CURRENCIES = [
    (KZT_MAP, KZT_DATA),
    (RUB_MAP, RUB_DATA),
    (KGS_MAP, KGS_DATA),
    (DOLLAR_MAP, DOLLAR_MAP),
    (EURO_MAP, EURO_MAP),
]

CURRENCY_MAP = {}

for currency, data in ALL_CURRENCIES:
    for currency_alias in currency:
        CURRENCY_MAP.update(currency_alias.lower(), data)
