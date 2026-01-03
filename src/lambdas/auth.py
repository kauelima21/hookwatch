from src.controllers.auth_controller import AuthController
from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse
from src.shared.http.router import Router


def handler(event: dict, _):
    http_request = HttpRequest(event)
    http_response = HttpResponse()

    router = Router()

    router.post("/auth/sign-in", AuthController, "sign_in")
    router.post("/auth/sign-up", AuthController, "sign_up")
    router.post("/auth/confirm-registration", AuthController, "confirm_registration")

    return router.dispatch(http_request, http_response)
