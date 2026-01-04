from src.controllers.organizations_controller import OrganizationsController
from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse
from src.shared.http.router import Router


def handler(event: dict, _):
    http_request = HttpRequest(event)
    http_response = HttpResponse()

    router = Router()

    router.get("/organizations", OrganizationsController, "index")
    router.post("/organizations", OrganizationsController, "store")

    return router.dispatch(http_request, http_response)
