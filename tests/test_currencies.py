import pytest

import src.money_transaction_params as handler_params
import src.currency_map as currency_map


class CurrencyAliasData:
    def __init__(self, alias, cur_data):
        self.alias = alias
        self.cur_data = cur_data
    
    alias = ''
    cur_data = ''


def get_all_cur_aliases():
    result = []
    for cur_alias in currency_map.CURRENCY_MAP:
        result.append(CurrencyAliasData(cur_alias, currency_map.CURRENCY_MAP[cur_alias]))

    return result


@pytest.mark.parametrize(
    'from_user, text, expected_params',
    [
        pytest.param(
            'user1',
            'give user2 10 ' + str(cur_alias_data.alias),
            handler_params.MoneyTransactionParams(
                def_cur_user = 'user1',
                from_user = 'user1',
                to_user = 'user2',
                money = float(10.0),
                cur_data = cur_alias_data.cur_data,
            ),
            id=f"check currency {cur_alias_data.cur_data.cur_name} alias {cur_alias_data.alias}",
        )
        for cur_alias_data in get_all_cur_aliases()
    ],
)
async def test_currencies(
    from_user,
    text,
    expected_params,
    get_tg_message,
    check_give_params_equal,
  ):
    msg = get_tg_message(from_user, text)

    params = await handler_params.get_money_transaction_params(msg)

    assert check_give_params_equal(params, expected_params)
