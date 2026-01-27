"""Runner which executes the main routine of Obscura."""

import logging
import time
from typing import Any

from obscura.core.rendering.rendering_pipeline import rendering_pipeline
from obscura.core.utilities import RunManager

log = logging.getLogger("obscura")


def run_obscura(config: Any) -> None:
    """General run procedure of Obscura.

    Args:
        config: Munch type object containing all configs for current
        run. Config options can be called via attribute-style access.
    """

    # Time
    start_time = time.time()

    # Run manager to handle overall tasks
    run_manager = RunManager(config)
    run_manager.init_run()

    # add overall execution here
    rendering_pipeline(config)

    # finalize run
    run_manager.finish_run(start_time)
