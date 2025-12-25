from src.shared.contracts.controller import BaseController
from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse


class ProjectsController(BaseController):
    def __init__(self, req: HttpRequest, res: HttpResponse) -> None:
        super().__init__(req, res)

    def index(self):
        return self.res.status(200).json({"message": "Hello World!"})

    def store(self):
        return self.res.status(201).json({"message": "Hello World!"})
