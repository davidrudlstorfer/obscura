"""Runner which executes the main routine of Obscura."""

import logging
import time
from typing import Any

# from obscura.core.example import exemplary_function
from obscura.core.render import render
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
    # log.info("Output of exemplary program: " + str(exemplary_function(2, 4)))
    render(config)

    # finalize run
    run_manager.finish_run(start_time)
