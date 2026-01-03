from src.models.auth import Auth
from src.models.user import User
from src.shared.contracts.base_error import BaseError
from src.shared.contracts.controller import BaseController
from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse


class AuthController(BaseController):
    def __init__(self, req: HttpRequest, res: HttpResponse) -> None:
        super().__init__(req, res)

    def sign_in(self) -> dict:
        try:
            email = self.req.body.get("email")
            password = self.req.body.get("password")

            auth = Auth()
            auth_result = auth.login(email, password)

            return self.res.json({
                "access_token": auth_result.access_token,
                "refresh_token": auth_result.refresh_token,
                "expires_in": auth_result.expires_in
            })
        except BaseError as e:
            return self.res.status(e.status_code).send(e.error_message)

    def sign_up(self) -> dict:
        try:
            full_name = self.req.body.get("full_name")
            email = self.req.body.get("email")
            password = self.req.body.get("password")

            user_already_exists = User().find_by_email(email)
            if user_already_exists:
                return self.res.status(401).send("Invalid Credentials")

            user = User()
            user.full_name = full_name
            user.email = email
            user.system_role = "member"
            user.status = "waiting"

            user.save()

            Auth().register(email, password)

            return self.res.status(201).send("User created")
        except BaseError as e:
            return self.res.status(e.status_code).send(e.error_message)

    def confirm_registration(self) -> dict:
        try:
            email = self.req.body.get("email")
            confirmation_code = self.req.body.get("confirmation_code")

            auth = Auth()
            auth.confirm_registration(email, confirmation_code)

            user = User().find_by_email(email)
            user.status = "active"
            user.save()

            return self.res.status(200).send("User confirmed")
        except BaseError as e:
            return self.res.status(e.status_code).send(e.error_message)
