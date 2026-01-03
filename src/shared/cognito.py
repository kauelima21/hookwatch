import boto3

from src.shared.constants import Env
from src.shared.contracts.auth import AuthenticationResult


class Cognito:
    def __init__(self):
        self._client = boto3.client("cognito-idp")

    def initiate_auth(self, email: str, password: str) -> AuthenticationResult:
        response = self._client.initiate_auth(
            ClientId=Env.HOOK_WATCH_COGNITO_CLIENT_ID,
            AuthFlow="USER_PASSWORD_AUTH",
            AuthParameters={"USERNAME": email, "PASSWORD": password},
        )

        auth_result = response["AuthenticationResult"]

        return AuthenticationResult(
            access_token=auth_result["AccessToken"],
            id_token=auth_result["IdToken"],
            refresh_token=auth_result["RefreshToken"],
            expires_in=auth_result["ExpiresIn"],
            token_type=auth_result["TokenType"],
        )

    def sign_up(self, email: str, password: str):
        response = self._client.sign_up(
            ClientId=Env.HOOK_WATCH_COGNITO_CLIENT_ID,
            Username=email,
            Password=password,
            UserAttributes=[
                {"Name": "email", "Value": email},
            ],
        )

        return response["UserSub"]

    def confirm_sign_up(self, email: str, confirmation_code: str):
        response = self._client.confirm_sign_up(
            ClientId=Env.HOOK_WATCH_COGNITO_CLIENT_ID,
            Username=email,
            ConfirmationCode=confirmation_code,
        )

        return response
