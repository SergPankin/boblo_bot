import pytest

import src.money_transaction_params as handler_params
import src.currency_map as currency_map


def reverse_expected_params(params):
    params.from_user, params.to_user = params.to_user, params.from_user


@pytest.mark.parametrize(
    'from_user, text, expected_params',
    [
        pytest.param(
          'user1',
          '/give user2 10',
          handler_params.MoneyTransactionParams(
              def_cur_user = 'user1',
              from_user = 'user1',
              to_user = 'user2',
              money = float(10.0),
              cur_data = '',
          ),
          id='test usual'
        ),
        pytest.param(
          'user1',
          '/give user2 10 t',
          handler_params.MoneyTransactionParams(
              def_cur_user = 'user1',
              from_user = 'user1',
              to_user = 'user2',
              money = float(10.0),
              cur_data = currency_map.KZT_DATA,
          ),
          id='test explicit separate currency'
        ),
        pytest.param(
          'user1',
          '/give user2 10t',
          handler_params.MoneyTransactionParams(
              def_cur_user = 'user1',
              from_user = 'user1',
              to_user = 'user2',
              money = float(10.0),
              cur_data = currency_map.KZT_DATA,
          ),
          id='test explicit solid currency'
        ),
        pytest.param(
          'user1',
          '/give user2 10 Some Comment',
          handler_params.MoneyTransactionParams(
              def_cur_user = 'user1',
              from_user = 'user1',
              to_user = 'user2',
              money = float(10.0),
              cur_data = '',
              comment = 'Some Comment',
          ),
          id='test comment without currency',
        ),
        pytest.param(
          'user1',
          '/give user2 10 t Some2 Comment',
          handler_params.MoneyTransactionParams(
              def_cur_user = 'user1',
              from_user = 'user1',
              to_user = 'user2',
              money = float(10.0),
              cur_data = currency_map.KZT_DATA,
              comment = 'Some2 Comment',
          ),
          id='test comment with separate currency',
        ),
        pytest.param(
          'user1',
          '/give user2 10t Some2 Comment',
          handler_params.MoneyTransactionParams(
              def_cur_user = 'user1',
              from_user = 'user1',
              to_user = 'user2',
              money = float(10.0),
              cur_data = currency_map.KZT_DATA,
              comment = 'Some2 Comment',
          ),
          id='test comment with solid currency',
        ),
    ]
)
@pytest.mark.parametrize(
  'is_take_handler', [False, True], 
)
async def test_give_params(
    from_user,
    text,
    expected_params,
    is_take_handler,
    get_tg_message,
    check_give_params_equal,
  ):
    if is_take_handler:
        reverse_expected_params(expected_params)
  
    msg = get_tg_message(from_user, text)

    params = await handler_params.get_money_transaction_params(msg, is_take_handler)

    assert check_give_params_equal(params, expected_params)


@pytest.mark.xfail
@pytest.mark.parametrize(
    'from_user, text',
    [
        pytest.param(
          'user1',
          '/give user2',
          id='test less arguments'
        ),
        pytest.param(
          'user1',
          '/give user2 tua',
          id='test wrong money'
        ),
    ]
)
async def test_wrong_history_params(
    from_user,
    text,
    get_tg_message,
  ):
    msg = get_tg_message(from_user, text)
    await handler_params.get_history_transaction_params(msg)
