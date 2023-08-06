from typing import Type

from lop_codeingame_cli.generator.base import AbstractGenerator
from lop_codeingame_cli.generator.python import PythonGenerator

generator: dict[str,  Type[AbstractGenerator]] = {
    "Python": PythonGenerator,
}