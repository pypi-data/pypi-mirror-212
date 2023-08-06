import os
import zipfile
from pathlib import Path
import requests
from tqdm import tqdm
from websocket import WebSocket


def read_file_in_chunks(file_path: Path, chunk_size: int = 1024*1024):
    with open(file_path, "rb") as file:
        while True:
            if chunk := file.read(chunk_size):
                yield chunk
            else:
                break



def to_zip(path: Path, zip_path: Path):
    with zipfile.ZipFile(zip_path, "w") as zipf:
        for root, _, files in os.walk(path):
            if Path(root) == zip_path.parent:
                continue
            for file in files:
                zipf.write(os.path.join(root, file), os.path.relpath(os.path.join(root, file), path))

def from_zip(zip_path: Path, path: Path):
    with zipfile.ZipFile(zip_path, "r") as zipf:
        zipf.extractall(path)


def send_file_to_api(base_path: Path, ws: WebSocket):
    temp_path = Path("temp")
    temp_path.mkdir(exist_ok=True)
    zip_path = temp_path / "archive.zip"
    to_zip(base_path, zip_path)
    file_size = os.path.getsize(zip_path)
    with tqdm(total=file_size, unit='B', unit_scale=True, desc="Uploading to serveur") as pbar:
        for part in read_file_in_chunks(zip_path):
            ws.send_binary(part)
            pbar.update(len(part))
    ws.close()
    zip_path.unlink()
    temp_path.rmdir()


def download_file_from_api(user_id: str, competition_id: str):
    kind = "template"
    url = f"http://localhost:8000/cli/lopdownload?user_id={user_id}&competition_id={competition_id}&kind={kind}"
    response = requests.get(url)
    return response.json()["download_link"]





