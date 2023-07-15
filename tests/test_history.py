import pytest

import src.history_transaction_params as handler_params
import src.currency_map as currency_map


@pytest.mark.parametrize(
    'from_user, text, expected_params',
    [
        pytest.param(
          'user1',
          '/history user2 10',
          handler_params.HistoryTransactionParams(
              from_user = 'user1',
              to_user = 'user2',
              cur_data = '',
              history_length = 10,
          ),
          id='test usual'
        ),
        pytest.param(
          'user1',
          '/history user2 *',
          handler_params.HistoryTransactionParams(
              from_user = 'user1',
              to_user = 'user2',
              cur_data = '',
              history_length = 0,
          ),
          id='test usual all'
        ),
        pytest.param(
          'user1',
          '/history user2 10 t',
          handler_params.HistoryTransactionParams(
              from_user = 'user1',
              to_user = 'user2',
              cur_data = currency_map.KZT_DATA,
              history_length = 10,
          ),
          id='test explicit currency'
        ),
    ]
)
async def test_history_params(
    from_user,
    text,
    expected_params,
    get_tg_message,
    check_history_params_equal,
  ):
    msg = get_tg_message(from_user, text)

    params = await handler_params.get_history_transaction_params(msg)

    assert check_history_params_equal(params, expected_params)


@pytest.mark.xfail
@pytest.mark.parametrize(
    'from_user, text',
    [
        pytest.param(
          'user1',
          '/history user2',
          id='test without length'
        ),
        pytest.param(
          'user1',
          '/history user2 t',
          id='test currency instead length'
        ),
        pytest.param(
          'user1',
          '/history user2 10 t 32',
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
    await handler_params.get_history_transaction_params(msg)
