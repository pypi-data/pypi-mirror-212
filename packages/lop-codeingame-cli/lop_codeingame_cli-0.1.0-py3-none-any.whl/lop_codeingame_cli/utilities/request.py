import json
from pathlib import Path

import requests

from lop_codeingame_cli.model.Exercise import Exercise
from lop_codeingame_cli.utilities.variables import CONFIG_PATH, get_base_url


def get_token() -> str:
    with open(CONFIG_PATH) as file:
        return json.load(file)["user_token"]

def get_headers() -> dict:
    return {"Authorization": f"Bearer {get_token()}"} if get_token() else {}

def get_exercise_id(base_path: Path) -> str:
    with open(base_path / "metadata.json") as file:
        return json.load(file)["exercise_id"]

def get_exercise_data(exercise_id: str) -> Exercise:
    response = requests.get(f"{get_base_url()}/exercises/{exercise_id}", headers=get_headers())
    return Exercise(**response.json())


# if __name__ == '__main__':
#     user_id = "Machkour"
#     competition_id = "2352"
#     # package_folder(user_id="Machkour", competition_id="2352", kind="template")
#     print(download_file_from_api(user_id=user_id, competition_id=competition_id))