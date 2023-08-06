from unittest.mock import patch

from .config import get_configuration_variable, bovine_client_config

from .test_store import store  # noqa F801


@patch("builtins.input")
async def test_get_configuration_variable(mock_input, store):  # noqa F401
    result = await get_configuration_variable("key")
    assert result is None
    mock_input.assert_not_called()

    mock_input.return_value = "value"
    result = await get_configuration_variable("key", "question")
    assert result == "value"
    mock_input.assert_called_once()

    result = await get_configuration_variable("key", "question")
    assert result == "value"
    mock_input.assert_called_once()


@patch("builtins.input")
async def test_bovine_client_config(mock_input, store):  # noqa F401
    mock_input.return_value = "name"
    await get_configuration_variable("activity_pub_host", "host")
    mock_input.return_value = "secret"
    await get_configuration_variable("private_key", "secret")

    result = await bovine_client_config()

    assert result == {"host": "name", "private_key": "secret"}
