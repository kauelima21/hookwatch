import logging

from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse


class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, method: str, path: str, handler, action=None):
        self.routes[method, path] = (handler, action)

    def dispatch(self, request: HttpRequest, response: HttpResponse):
        method = request.method
        path = request.path

        route = self.routes.get((method, path))
        if not route:
            logging.warning(f"Route not found: {method} {path}")
            return response.status(404).send("Not Found")

        handler, action = route
        handler_response = handler(request, response)
        if action:
            return getattr(handler_response, action)()

        if not isinstance(handler_response, dict):
            return handler_response()

        return handler_response

    def get(self, path: str, handler, action=None):
        self.add_route("GET", path, handler, action)

    def post(self, path: str, handler, action=None):
        self.add_route("POST", path, handler, action)

    def put(self, path: str, handler, action=None):
        self.add_route("PUT", path, handler, action)

    def delete(self, path: str, handler, action=None):
        self.add_route("DELETE", path, handler, action)

    def patch(self, path: str, handler, action=None):
        self.add_route("PATCH", path, handler, action)

    def options(self, path: str, handler, action=None):
        self.add_route("OPTIONS", path, handler, action)

    def head(self, path: str, handler, action=None):
        self.add_route("HEAD", path, handler, action)
