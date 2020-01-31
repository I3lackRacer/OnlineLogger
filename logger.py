import os

import requests

log_to = os.getenv("LOG_URL")
if not log_to:
    log_to = "localhost"

tenant = os.getenv("TENANT")
if not tenant:
    tenant = "default"


def info(msg: str) -> requests.Response:
    data = {
        "tenant": tenant,
        "message": msg
    }
    print("INFO " + msg)
    return requests.post(log_to + ":4308/info", json=data)


def error(msg: str) -> requests.Response:
    data = {
        "tenant": tenant,
        "message": msg
    }
    print("ERROR " + msg)
    return requests.post(log_to + ":4308/error", json=data)


def warn(msg: str) -> requests.Response:
    data = {
        "tenant": tenant,
        "message": msg
    }
    print("WARN " + msg)
    return requests.post(log_to + ":4308/warn", json=data)
