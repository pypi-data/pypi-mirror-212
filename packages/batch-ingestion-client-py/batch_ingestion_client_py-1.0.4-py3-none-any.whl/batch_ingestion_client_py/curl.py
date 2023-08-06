from typing import Literal
from urllib.parse import quote
import subprocess
import json

Method = Literal["GET", "POST", "PUT", "DELETE"]


def exec(command: str) -> str:
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    stdout, stderr = process.communicate()

    if process.returncode != 0:
        raise Exception(stderr.decode("utf-8"))

    return stdout.decode("utf-8")


def curl(
    method: Method,
    url: str,
    cookie_file: str,
    form_data: dict | None = None,
    json_data: dict | None = None,
):
    is_json = json_data is not None

    json_data = json_data if json_data is not None else {}
    form_data = form_data if form_data is not None else {}

    header = (
        "application/json"
        if is_json else
        "application/x-www-form-urlencoded"
    )
    data = (
        json.dumps(json_data)
        if is_json else
        "&".join([
            f"{ quote(key) }={ quote(value) }"
            for key, value in form_data.items()
        ])
    )

    curlCommand = f"""
        curl -X { method } \
            -H "Content-Type: { header }" \
            -c { cookie_file } \
            -b { cookie_file } \
            -d '{ data }' \
            \"{ url }\"
    """.strip()

    data = exec(curlCommand)

    try:
        return json.loads(data)
    except Exception:
        raise Exception(data)
