from importlib import import_module, resources
from importlib.metadata import version
from typing import Any, Callable
from pathlib import Path

from yaml import safe_load

__version__: str = version("un_yaml")

class UnYaml:
    KEY = "_yaml"
    SEP = "/"
    PREFIX = "#/"
    REF = "$ref"
    REF_ERROR = f"Value for Key {REF} does not start with {PREFIX}"
    DEFAULT = "data.yaml"
    DEFAULT_INFO = {
        "_version": __version__,
        "app": "data-yaml",
        "app_version": "0.0.1",
        "doc": __name__,
        "doc_version": "0.0.1",
    }

    @classmethod
    def LoadYaml(cls, filename: str, pkg: str, sub: str = "") -> dict:
        yaml_dir = resources.files(pkg)
        if len(sub) > 0:
            yaml_dir = yaml_dir / sub
        yaml_file = yaml_dir / filename
        yaml_string = yaml_file.read_text()
        yaml_data = safe_load(yaml_string)
        return yaml_data

    @classmethod
    def NewYaml(cls, info={}) -> dict:
        opts = UnYaml.DEFAULT_INFO | {"doc": cls.__name__} | info
        yaml_data = {UnYaml.KEY: opts}
        return yaml_data

    @classmethod
    def ReadYaml(cls, path: Path, defaults={}) -> dict:
        if not path.exists():
            return cls.NewYaml(defaults)
        yaml_string = path.read_text()
        yaml_data = safe_load(yaml_string)

        if not yaml_data:
            return cls.NewYaml(defaults)
        return yaml_data

    def __init__(self, yaml_data: dict) -> None:
        self.data = yaml_data
        assert self.data, "UnYaml: no data"
        self._info = self.data[UnYaml.KEY]

    def info(self, key: str) -> Any:
        return self._info.get(key)

    def expand(self, item):
        if isinstance(item, dict):
            if UnYaml.REF in item:
                return self._expand(item)
            return {k: self.expand(v) for (k, v) in item.items()}
        if isinstance(item, list):
            return [self.expand(v) for v in item]
        return item

    def _expand(self, item):
        ref = item[UnYaml.REF]
        if not ref.startswith(UnYaml.PREFIX):
            raise ValueError(f"cannot expand {ref}: {UnYaml.REF_ERROR}")
        value = self.get(ref[2:])
        for key in item:
            if key != UnYaml.REF:
                value[key] = item[key]
        return self.expand(value)

    def _get(self, result, key: str):
        if not result:
            return False
        if isinstance(result, list):
            return result[int(key)]
        return result.get(key)

    def get(self, keylist: str) -> Any:
        result = self.data
        for key in keylist.split(UnYaml.SEP):
            item = self._get(result, key)
            result = self.expand(item)

        return result

    def get_handler(self, key: str) -> Callable:
        handlers = self.info("handlers")
        handler = handlers.get(key)
        if not handler:
            raise ValueError(f"UnYaml.get_handler: no handler for {key}")

        module = import_module(handler["module"])
        return getattr(module, handler["method"])
