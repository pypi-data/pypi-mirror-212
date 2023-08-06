from enum import Enum
from typing import Annotated

import requests
import typer

from lop_codeingame_cli.generator import generator
from lop_codeingame_cli.model.Exercise import Exercise
from lop_codeingame_cli.utilities.request import get_headers
from lop_codeingame_cli.utilities.variables import get_base_url


class Language(str, Enum):
    PYTHON = "python"
id_exo = "647a9115366d4ba3edb6b380"



def lopgenerate(
        exercise: Annotated[str, typer.Option(help="L'id de l'exercice")],
):
    response = requests.get(
        f"{get_base_url()}/cli/lopgenerate/{exercise}",
        headers=get_headers(),
    )
    if response.status_code == 200:
        try:
            data = Exercise(**response.json())
            generator[data.language.value](exercise=data).generate()
            print("Le répertoire a été créé avec succès")
        except FileExistsError:
            print("Le répertoire existe déjà")
    else:
        print(response.json()["detail"])



if __name__ == '__main__':
    typer.run(lopgenerate)
