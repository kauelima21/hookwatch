from src.controllers.projects_controller import ProjectsController
from src.shared.contracts.base_error import BaseError
from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse
from src.shared.http.router import Router


def handler(event: dict, _):
    http_request = HttpRequest(event)
    http_response = HttpResponse()

    try:
        router = Router()

        router.get("/organizations/{organization_id}/projects", ProjectsController, "index")
        router.get("/organizations/{organization_id}/projects/{project_id}", ProjectsController, "show")
        router.post("/organizations/{organization_id}/projects", ProjectsController, "store")

        return router.dispatch(http_request, http_response)
    except BaseError as e:
        return http_response.status(e.status_code).send(e.error_message)
