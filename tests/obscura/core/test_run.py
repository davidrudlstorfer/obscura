"""Test run procedure."""

from unittest.mock import MagicMock, patch

from munch import munchify

from obscura.core.run import run_obscura


def test_run_obscura() -> None:
    """Test run procedure of Obscura."""

    mock_config = munchify({"key": "value"})

    mock_run_manager = MagicMock()

    with patch("obscura.core.run.RunManager", return_value=mock_run_manager):
        mock_exemplary_function = MagicMock(return_value="Exemplary output")
        with patch("obscura.core.run.exemplary_function", mock_exemplary_function):
            run_obscura(mock_config)

    mock_run_manager.init_run.assert_called_once()
    mock_exemplary_function.assert_called_once()
    mock_run_manager.finish_run.assert_called_once()
