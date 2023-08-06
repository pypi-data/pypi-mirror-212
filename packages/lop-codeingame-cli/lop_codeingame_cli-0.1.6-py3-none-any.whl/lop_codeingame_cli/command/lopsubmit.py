from pathlib import Path
from typing import Annotated

import requests
import typer
from websocket import create_connection, WebSocketBadStatusException

from lop_codeingame_cli.enumerations.main import SubmissionKind
from lop_codeingame_cli.utilities.file import send_file_to_api
from lop_codeingame_cli.utilities.request import get_headers, get_exercise_id
from lop_codeingame_cli.utilities.variables import get_web_socket_url


def send_files_to_server(config_file_path: str, main_file_path, test_file_path, server_url):
    files = {
        'config': open(config_file_path, 'rb'),
        'main': open(main_file_path, 'rb'),
        'test': open(test_file_path, 'rb')
    }

    response = requests.post(server_url, files=files)

    for file in files.values():
        file.close()
    return response.status_code


def lopsubmit(
        path: Annotated[str, typer.Option(help="Le chemin vers le répertoire de l'exercice")] = ".",
        kind: Annotated[SubmissionKind, typer.Option(help="Le type de soumission (solve ou template)")] = "solve",
):
    base_path = Path(path).absolute()

    if not base_path.exists():
        print("Le chemin spécifié n'existe pas")
        return
    if not (config_path:=(base_path / ".lopcodeingame")).exists():
        print("Le chemin spécifié ne contient pas de fichier de configuration")
        return
    exercise_id = get_exercise_id(config_path)
    try:
        headers = get_headers()["Authorization"]
        ws = create_connection(f"{get_web_socket_url()}/cli/lopsubmit?kind={kind}&exercise_id={exercise_id}",
                               header=[
                                   f"Authorization: {headers}"
                               ])
        send_file_to_api(base_path, ws)
    except WebSocketBadStatusException:
        print('WebSocket connection failed: HTTP 403 Forbidden')

def run():
    typer.run(lopsubmit)
if __name__ == '__main__':
    run()
