import json


class HttpRequest:
    def __init__(self, event: dict) -> None:
        self.request_context = event["requestContext"]
        self.raw_path = event["rawPath"]
        self.path = event["routeKey"].split(" ")[1]
        self.query = event.get("queryStringParameters", {})
        self.params = event.get("pathParameters", {})
        self.headers = event["headers"]
        self.body = json.loads(event.get("body", "{}"))
        self.raw_body = event.get("body", "{}")
        self.method = self.request_context["http"]["method"]
