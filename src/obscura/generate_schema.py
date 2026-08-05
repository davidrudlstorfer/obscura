"""Generate JSON schema for Obscura configuration."""

import json

from obscura.core.config_model import Configuration


def generate_schema() -> None:
    """Generate and save JSON schema."""
    schema = Configuration.model_json_schema()

    with open("config_schema.json", "w") as file:
        json.dump(schema, file, indent=2)


if __name__ == "__main__":
    generate_schema()
