from datetime import datetime
from pathlib import Path
from typing import List, Dict
from starlette.exceptions import HTTPException

import yaml
from fastapi import FastAPI, Header
import uvicorn as uvicorn


def load_config() -> Dict:
    with open('config.yml') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return data


app = FastAPI(title="logger")
save_directory: str
config = load_config()


def save_info(tenant: str,  msg: str):
    save_log(tenant, "INFO", msg)


def save_error(tenant: str,  msg: str):
    save_log(tenant, "ERROR", msg)


def save_warning(tenant: str,  msg: str):
    save_log(tenant, "WARN", msg)


def save_log(tenant: str, lvl: str,  msg: str):
    tenant = tenant.lower()
    absolute_dir = save_directory + tenant + "/"
    Path(absolute_dir).mkdir(parents=True, exist_ok=True)
    time = datetime.now()
    time_string = time.strftime("%d.%m.%Y, %H:%M:%S")
    log_message = f"[{time_string}]\t{lvl.upper()}\t>>> {msg}"
    file_name = tenant + " - " + time.strftime("%d.%m.%Y") + ".log"
    with open(absolute_dir + file_name, "a") as log_file:
        log_file.write(log_message + "\n")


def setup_api():
    @app.post("/info")
    def info(*, authorization: str = Header(None), payload: Dict):
        tenant, msg = check(payload, authorization)
        return save_info(tenant, msg)
    pass

    @app.post("/error")
    def error(*, authorization: str = Header(None), payload: Dict):
        tenant, msg = check(payload, authorization)
        return save_error(tenant, msg)

    @app.post("/warning")
    def warn(*, authorization: str = Header(None), payload: Dict):
        tenant, msg = check(payload, authorization)
        return save_warning(tenant, msg)


def check(payload: Dict, authorization: str = Header(None)) -> (str, str):
    tenant = payload.get("tenant")
    if not tenant:
        raise HTTPException(422, "Missing 'tenant' key in payload")
    msg = payload.get("message")
    if not msg:
        raise HTTPException(422, "Missing 'message' key in payload")
    if not authorization:
        raise HTTPException(422, "Missing 'authorization' key in headers")
    if authorization != config["authorization"]:
        raise HTTPException(403, "Invalid authorization key")
    return tenant, msg


setup_api()

if __name__ == '__main__':
    print("Starting Service")
    save_directory = config["safe-directory"]
    uvicorn.run(app, host="0.0.0.0", port=4308)
