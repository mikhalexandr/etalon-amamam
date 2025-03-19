import importlib
import os
import pkgutil
from typing import List


def load_all_models(module_paths: List[str]) -> None:
    for module_path in module_paths:
        package = importlib.import_module(module_path)
        package_path = os.path.dirname(package.__file__)

        for _, module_name, is_pkg in pkgutil.iter_modules([package_path]):
            if not is_pkg:
                full_module_name = f"{module_path}.{module_name}"
                importlib.import_module(full_module_name)
