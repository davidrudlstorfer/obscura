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
    if "--" in argv:  # If called with Docker/Blender
        argv = argv[argv.index("--") + 1 :]
    else:
        argv = []  # If called with "obscura"

    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument(
        "--config_file_path",
        "-cfp",
        help="Path to config file.",
        type=str,
        required=False,
    )

    args = parser.parse_args(argv)

    # If no argument was provided: use default config
    if args.config_file_path is None:
        print("No config file provided, using default config.")
        args.config_file_path = "src/obscura/configs/params.yaml"
    else:
        print("Obscura executed from given config file")

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
