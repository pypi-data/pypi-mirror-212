from lop_codeingame_cli.generator.base import AbstractGenerator
from lop_codeingame_cli.model.Exercise import Exercise

main_content= """
def main():
    return "Hello World"
"""
test_content = """
import unittest
from src.main import main
class TestMain(unittest.TestCase):
    def test_main(self):
        self.assertEqual(main(), "Hello World")
"""
class PythonGenerator(AbstractGenerator):
    def __init__(self, exercise: Exercise):
        super().__init__(exercise)
        self.main_content = main_content
        self.test_content = test_content
    def generate(self):
        main_src_path = self.src_path / "main.py"
        main_test_path = self.test_path / "test_main.py"
        with open(main_src_path, "w") as f:
            f.write(main_content)
        with open(main_test_path, "w") as f:
            f.write(test_content)
        self.generate_config_folder()
