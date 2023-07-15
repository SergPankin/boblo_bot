import pytest

import src.balance_params as handler_params
import src.currency_map as currency_map


@pytest.mark.parametrize(
    'from_user, text, expected_params',
    [
        pytest.param(
          'user1',
          '/balance user2',
          handler_params.BalanceParams(
              from_user = 'user1',
              to_user = 'user2',
              cur_data = '',
          ),
          id='test usual'
        ),
        pytest.param(
          'user1',
          '/balance user2 t',
          handler_params.BalanceParams(
              from_user = 'user1',
              to_user = 'user2',
              cur_data = currency_map.KZT_DATA,
          ),
          id='test with explicit currency'
        ),
    ]
)
async def test_history_params(
    from_user,
    text,
    expected_params,
    get_tg_message,
    check_balance_params_equal,
  ):
    msg = get_tg_message(from_user, text)

    params = await handler_params.get_balance_params(msg)

    assert check_balance_params_equal(params, expected_params)


@pytest.mark.xfail
@pytest.mark.parametrize(
    'from_user, text',
    [
        pytest.param(
          'user1',
          '/balance',
          id='test without user'
        ),
        pytest.param(
          'user1',
          '/balance user2 10',
          id='test wrong currency'
        ),
        pytest.param(
          'user1',
          '/balance user2 uoa 35',
          id='test more params'
        ),
    ]
)
async def test_wrong_history_params(
    from_user,
    text,
    get_tg_message,
  ):
    msg = get_tg_message(from_user, text)
    await handler_params.get_balance_params(msg)
