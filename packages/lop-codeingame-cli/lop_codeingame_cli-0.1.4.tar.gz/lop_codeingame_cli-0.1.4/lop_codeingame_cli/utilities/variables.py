from pathlib import Path

IS_LOCAL=True
BASE="localhost:8000"
BASE_REMOTE="lopcodeingame.herokuapp.com"
APP_PATH: Path = Path("~/lopcodeingame").expanduser()
CONFIG_PATH: Path =  APP_PATH / "config.json"

def get_base_url() -> str:
    return f"http://{BASE}" if IS_LOCAL else f"https://{BASE_REMOTE}"

def get_web_socket_url() -> str:
    return f"ws://{BASE}" if IS_LOCAL else f"wss://{BASE_REMOTE}"