from pathlib import Path
import yaml

from obscura.core.config_model import Configuration


CONFIG_PATH = Path(__file__).parents[1] / "src" / "obscura" / "configs" / "params.yaml"


with CONFIG_PATH.open("r") as file:
    data = yaml.safe_load(file)


config = Configuration.model_validate(data)


def test_config_model():
    assert isinstance(config, Configuration)