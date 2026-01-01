from src.models.auth import Auth
from src.models.user import User
from src.shared.contracts.controller import BaseController
from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse


class AuthController(BaseController):
    def __init__(self, req: HttpRequest, res: HttpResponse) -> None:
        super().__init__(req, res)

    def sign_in(self) -> dict:
        email = self.req.body.get("email")
        password = self.req.body.get("password")

        user_already_exists = User().find_by_email(email)
        if user_already_exists:
            return self.res.status(409).send("User already exists")

        auth = Auth()
        auth_result = auth.login(email, password)

        return self.res.json({
            "access_token": auth_result.access_token,
            "refresh_token": auth_result.refresh_token,
            "expires_in": auth_result.expires_in
        })
