import pytest

import src.default_params as handler_params
import src.currency_map as currency_map


@pytest.mark.parametrize(
    'user, text, expected_params',
    [
        pytest.param(
          'user1',
          '/default t',
          handler_params.DefaultParams(
              user = 'user1',
              cur_data = currency_map.KZT_DATA,
          ),
          id='test usual'
        ),
    ]
)
async def test_history_params(
    user,
    text,
    expected_params,
    get_tg_message,
    check_default_params_equal,
  ):
    msg = get_tg_message(user, text)

    params = await handler_params.get_default_params(msg)

    assert check_default_params_equal(params, expected_params)


@pytest.mark.xfail
@pytest.mark.parametrize(
    'user, text',
    [
        pytest.param(
          'user1',
          '/default',
          id='test without currency'
        ),
        pytest.param(
          'user1',
          '/default 10',
          id='test wrong currency'
        ),
        pytest.param(
          'user1',
          '/default t uec',
          id='test more params'
        ),
        pytest.param(
          'user1',
          '/default user1 t',
          id='test excess user'
        ),
    ]
)
async def test_wrong_history_params(
    user,
    text,
    get_tg_message,
  ):
    msg = get_tg_message(user, text)
    await handler_params.get_default_params(msg)
