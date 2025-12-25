import json


class HttpResponse:
    def __init__(self) -> None:
        self.status_code = 200
        self.headers = {}
        self.cookies = []
        self.body = None

    def status(self, status_code: int):
        self.status_code = status_code
        return self

    def send(self, body: str):
        self.body = body
        if not self.headers.get("Content-Type"):
            self.headers["Content-Type"] = "text/plain"
        return self._finalize()

    def json(self, body: dict | list):
        self.headers["Content-Type"] = "application/json"
        self.body = json.dumps(body)
        return self._finalize()

    def set(self, key: str, value: str):
        self.headers[key] = str(value)
        return self

    def cookie(self, cookie: str):
        self.cookies.append(cookie)
        return self

    def _finalize(self) -> dict:
        response = {
            "statusCode": self.status_code,
            "headers": dict(self.headers),
            "isBase64Encoded": False,
        }

        if self.cookies:
            response["cookies"] = self.cookies

        if self.body is not None:
            response["body"] = self.body

        return response
