"""Test run procedure."""

from unittest.mock import MagicMock, patch

from munch import munchify

from obscura.core.run import run_obscura


def test_run_obscura() -> None:
    """Test run procedure of Obscura."""

    mock_config = munchify({"key": "value"})

    mock_run_manager = MagicMock()

    # patch RunManager and rendering_pipeline
    with (
        patch("obscura.core.run.RunManager", return_value=mock_run_manager),
        patch("obscura.core.run.rendering_pipeline") as mock_pipeline,
    ):
        run_obscura(mock_config)

        # check RunManager methods called
        mock_run_manager.init_run.assert_called_once()
        mock_run_manager.finish_run.assert_called_once()
        args, _ = mock_run_manager.finish_run.call_args
        assert isinstance(args[0], float)

        # check rendering pipeline called correctly
        mock_pipeline.assert_called_once_with(mock_config)
