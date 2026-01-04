from src.models.auth import Auth
from src.models.organization import Organization
from src.models.organization_user import OrganizationUser
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

        auth = Auth()
        auth_result = auth.login(email, password)

        return self.res.json({
            "access_token": auth_result.access_token,
            "refresh_token": auth_result.refresh_token,
            "expires_in": auth_result.expires_in,
            "id_token": auth_result.id_token
        })

    def sign_up(self) -> dict:
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

    def confirm_registration(self) -> dict:
        email = self.req.body.get("email")
        confirmation_code = self.req.body.get("confirmation_code")

        auth = Auth()
        auth.confirm_registration(email, confirmation_code)

        user = User().find_by_email(email)
        user.status = "active"
        user.save()

        organization = Organization()
        organization.name = user.full_name
        organization.save()

        organization_user = OrganizationUser()
        organization_user.organization_id = organization.organization_id
        organization_user.user = email
        organization_user.organization_name = organization.name
        organization_user.user_full_name = user.full_name
        organization_user.save()

        return self.res.status(200).send("User confirmed")
