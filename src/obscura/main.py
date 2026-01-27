"""Main routine of Obscura."""

import argparse
import os
import sys

sys.path.append("/workspace/src")
sys.path.append("/workspace/src/pytoda/src")  # Otherwise, can't use Pytoda properly

import yaml
from munch import munchify

from obscura.core.run import run_obscura


def main() -> None:
    """Call Obscura runner with config.

    Raises:
        RuntimeError: If provided config is not a valid file.
    """
    argv = sys.argv
    if "--" in argv:
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []

    parser = argparse.ArgumentParser(description="Execute Obscura")
    parser.add_argument(
        "--config_file_path",
        "-cfp",
        help="Path to config file.",
        type=str,
        required=True,
    )

    args = parser.parse_args(argv)

    # load config and convert to simple namespace for easier access
    if not os.path.isfile(args.config_file_path):
        raise RuntimeError(f"Config file not found at {args.config_file_path}")

    with open(args.config_file_path, "r") as file:
        config = munchify(yaml.safe_load(file))

    # execute obscura
    run_obscura(config)


if __name__ == "__main__":  # pragma: no cover
    main()
    exit(0)
