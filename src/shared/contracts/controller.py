from abc import ABC

from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse


class BaseController(ABC):
    def __init__(self, req: HttpRequest, res: HttpResponse):
        self.req = req
        self.res = res
