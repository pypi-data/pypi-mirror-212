from os import getenv
from dotenv.main import load_dotenv
from os.path import exists
import json
from pathlib import Path
from dsutils_ms.helpers.log import log_title


def load_env():
    PATH = "./"

    while True:
        if exists(PATH + ".env"):
            load_dotenv(Path(PATH + ".env"))
            log_title("Loading .env file")
            break
        if exists(PATH + ".gitignore"):
            break
        PATH = "../" + PATH

    if not exists(PATH + ".env"):
        raise Exception(".env file not found")


def get_credential(key: str) -> str:
    load_env()

    data = getenv(key)

    if data is None:
        raise Exception(f"Environment variable {key} not found")

    JSON_CREDENTIALS = ["GOOGLE_SERVICE_ACCOUNT"]
    if key in JSON_CREDENTIALS:
        data = data.replace("\\\\n", "\\n")
        data = json.loads(data)

    return data
