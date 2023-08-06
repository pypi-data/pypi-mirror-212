import json
from pathlib import Path
from typing import Annotated
import re

import requests
import typer
from lop_codeingame_cli.utilities.variables import get_base_url, APP_PATH, CONFIG_PATH


def save_token_locally(token: str) -> None:
    app_path = Path(APP_PATH).expanduser()
    app_path.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w") as file:
        json.dump({"user_token": token}, file)


def is_valid_mail(mail: str):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if bool(re.fullmatch(regex, mail)):
        return mail
    raise typer.BadParameter("Adresse mail invalide")


def lopauth(
        mail: Annotated[str, typer.Option(...,
                                          help="Votre adresse mail",
                                          prompt=True,
                                          callback=is_valid_mail
                                          )],
        password: Annotated[str, typer.Option(..., help="Votre mot de passe", prompt=True, hide_input=True)],
):
    response = requests.post(
        f"{get_base_url()}/auth/login",
        json={"mail": mail, "password": password},
    )
    if response.status_code == 200:
        print("Vous êtes connecté")
        auth_token = response.json().get("detail").get("auth_token")
        save_token_locally(auth_token)
    elif response.status_code in {401, 404}:
        print(response.json()["detail"])
    else:
        print("Une erreur du serveur est survenue")

def run():
    typer.run(lopauth)

if __name__ == '__main__':
    typer.run(lopauth)
