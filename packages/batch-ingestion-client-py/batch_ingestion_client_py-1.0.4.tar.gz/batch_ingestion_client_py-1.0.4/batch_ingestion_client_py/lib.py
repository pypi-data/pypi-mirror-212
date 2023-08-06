from batch_ingestion_client_py.data import Entity
from batch_ingestion_client_py.response import Response
from batch_ingestion_client_py.curl import curl
from typing import List


DEFAULT_COOKIE_FILE = "cookies.txt"


class BatchIngestor:
    def __init__(
        self,
        base_url: str,
        username: str,
        password: str,
        cookie_file: str = DEFAULT_COOKIE_FILE,
    ):
        self.base_url = base_url
        self.cookie_file = cookie_file
        self.logged_in = False
        self._login(username, password)

    def _login(self, username: str, password: str):
        url = f"{ self.base_url }/w/api.php"
        res = curl(
            "POST",
            url,
            self.cookie_file,
            form_data={
                "action": "query",
                "meta": "tokens",
                "type": "login",
                "format": "json",
            },
        )
        login_token = res["query"]["tokens"]["logintoken"]
        res = curl(
            "POST",
            url,
            self.cookie_file,
            form_data={
                "action": "login",
                "lgname": username,
                "lgpassword": password,
                "lgtoken": login_token,
                "format": "json",
            },
        )
        login = res["login"]
        if login["result"] != "Success":
            raise Exception(f"Login failed: { login['reason'] }")
        self.logged_in = True

    def ingest(self, entities: List[Entity]):
        if not self.logged_in:
            raise Exception("You must be logged in to ingest entities")
        url = f"{ self.base_url }/w/rest.php/BatchIngestion/v0/batchcreate"
        json_data = {
            "entities": [entity.serialize() for entity in entities],
        }
        res = curl(
            "POST",
            url,
            self.cookie_file,
            json_data=json_data,
        )
        return Response.parse(res)
