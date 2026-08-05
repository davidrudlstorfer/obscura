"""Test main."""

from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
import yaml

from obscura.main import main


def test_main_config_file_exists(tmp_path: Path) -> None:
    """Test main when config exists.

    Args:
        tmp_path (Path): Temporary path from pytest.
    """
    # Use the existing valid configuration as test input
    with open("src/obscura/configs/params.yaml", "r") as file:
        mock_config_data = yaml.safe_load(file)

    config_file_path = tmp_path / "test_config.yaml"

    with open(config_file_path, "w") as file:
        yaml.dump(mock_config_data, file)

    with (
        patch(
            "argparse.ArgumentParser.parse_args",
            return_value=MagicMock(config_file_path=str(config_file_path)),
        ),
        patch("obscura.main.run_obscura") as mock_run_obscura,
    ):
        main()

        # Check that run_obscura was called with a Configuration object
        mock_run_obscura.assert_called_once()

        captured_config = mock_run_obscura.call_args[0][0]

        assert captured_config.general is not None


def test_main_config_file_not_exists() -> None:
    """Test main when config does not exist."""
    with patch(
        "argparse.ArgumentParser.parse_args",
        return_value=MagicMock(config_file_path="nonexistent_config.yaml"),
    ):
        with pytest.raises(
            RuntimeError,
            match="Config file not found!",
        ):
            main()
