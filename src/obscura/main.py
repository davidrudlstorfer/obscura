"""Main routine of Obscura."""

import argparse
import os

import yaml

from obscura.core.config_model import Configuration
from obscura.core.run import run_obscura


def main() -> None:
    """Call Obscura runner with config.

    Raises:
        RuntimeError: If provided config is not a valid file.
    """

    parser = argparse.ArgumentParser(description="Execute Obscura")
    parser.add_argument(
        "--config_file_path",
        "-cfp",
        help="Path to config file.",
        type=str,
        required=True,
    )

    args = parser.parse_args()

    if not os.path.isfile(args.config_file_path):
        raise RuntimeError("Config file not found! Obscura can not be executed!")

    with open(args.config_file_path, "r") as file:
        data = yaml.safe_load(file)

    config = Configuration.model_validate(data)

    run_obscura(config)


if __name__ == "__main__":  # pragma: no cover
    main()
    exit(0)