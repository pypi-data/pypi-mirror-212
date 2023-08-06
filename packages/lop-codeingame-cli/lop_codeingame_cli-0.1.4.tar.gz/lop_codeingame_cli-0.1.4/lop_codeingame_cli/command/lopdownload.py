from pathlib import Path

from enum import Enum
from typing import Annotated

import requests
import typer

from lop_codeingame_cli.utilities.file import from_zip
from lop_codeingame_cli.utilities.request import get_exercise_data, get_headers
from lop_codeingame_cli.utilities.variables import get_base_url


class DownloadKind(str, Enum):
    solve = 'solve'
    template = 'template'


def lopdownload(

        exercise_id: Annotated[str,typer.Option(..., help="Id de l'exercise")],
):
    exercise = get_exercise_data(exercise_id)
    base_path = Path(exercise.name).absolute()
    base_path.mkdir(exist_ok=True)
    response = requests.get(
        f"{get_base_url()}/cli/lopdownload?exercise_id={exercise_id}",
        headers=get_headers(),
    )
    if response.status_code == 200:
        extract_zip_file(response, base_path)
    else:
        print("Une erreur est survenue lors du téléchargement du fichier: " + response.json()["detail"])



def extract_zip_file(response, base_path):
    download_link = response.json()["download_link"]
    response = requests.get(download_link, stream=True)
    zip_path = base_path / "archives.zip"
    with open(zip_path, "wb") as file:
        file.write(response.content)
    from_zip(zip_path, base_path)
    zip_path.unlink()
    print(f"Le fichier a été téléchargé dans {base_path}")

def run():
    typer.run(lopdownload)

if __name__ == '__main__':
    run()
