import pytest


from aiogram import types


@pytest.fixture
def get_tg_message():
    def _make_tg_msg(from_username, from_message):
        msg = types.Message
        msg.from_user = types.User
        msg.from_user.username = from_username
        msg.text = from_message
        return msg
    return _make_tg_msg

@pytest.fixture
def check_give_params_equal():
    def _check_equal(params, exp_params):
        assert params.from_user == exp_params.from_user
        assert params.to_user == exp_params.to_user
        assert params.def_cur_user == exp_params.def_cur_user
        assert params.money == exp_params.money
        assert params.cur_data == exp_params.cur_data
        assert params.comment == exp_params.comment
        return True
    return _check_equal


@pytest.fixture
def check_history_params_equal():
    def _check_equal(params, exp_params):
        assert params.from_user == exp_params.from_user
        assert params.to_user == exp_params.to_user
        assert params.history_length == exp_params.history_length
        assert params.cur_data == exp_params.cur_data
        return True
    return _check_equal


@pytest.fixture
def check_balance_params_equal():
    def _check_equal(params, exp_params):
        assert params.from_user == exp_params.from_user
        assert params.to_user == exp_params.to_user
        assert params.cur_data == exp_params.cur_data
        return True
    return _check_equal


@pytest.fixture
def check_default_params_equal():
    def _check_equal(params, exp_params):
        assert params.user == exp_params.user
        assert params.cur_data == exp_params.cur_data
        return True
    return _check_equal
