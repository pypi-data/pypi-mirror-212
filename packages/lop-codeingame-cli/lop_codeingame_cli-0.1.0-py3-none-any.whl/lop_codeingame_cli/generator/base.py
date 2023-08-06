import json
from pathlib import Path

from lop_codeingame_cli.model.Exercise import Exercise
from abc import ABC, abstractmethod


class AbstractGenerator(ABC):
    def __init__(self, exercise: Exercise):
        self.base_path = Path(exercise.name)
        self.base_path.mkdir(exist_ok=True)
        self.exercise = exercise
        self.main_content: str = ""
        self.test_content: str = ""

    @abstractmethod
    def generate(self) -> None:
        pass

    @property
    def src_path(self) -> Path:
        path = self.base_path / "src"
        path.mkdir()
        return path

    @property
    def test_path(self) -> Path:
        path = self.base_path / "test"
        path.mkdir(exist_ok=True)
        return path

    @property
    def config_path(self):
        path = self.base_path / ".lopcodeingame"
        path.mkdir(exist_ok=True)
        return path

    @property
    def metadata_path(self):
        return self.config_path / "metadata.json"

    @property
    def settings_path(self):
        return self.config_path / "settings.json"

    def generate_metadata(self):
        with open(self.metadata_path, "w") as file:
            data = {
                "exercise_id": self.exercise.id,
                "owner": self.exercise.owner,
            }
            json.dump(data, file)

    def generate_settings(self):
        with open(self.settings_path, "w") as file:
            data = {
                "name": self.exercise.name,
                "files": {
                    "solution": [
                        "src/main.py"
                    ],
                    "test": [
                        "test/test_main.py",
                    ],

                },

            }
            json.dump(data, file)

    def generate_config_folder(self) -> None:
        self.generate_metadata()
        self.generate_settings()
