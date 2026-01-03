import logging

from src.shared.cognito import Cognito
from src.shared.errors import UnauthorizedError


class Auth:
    def __init__(self) -> None:
        self._cognito = Cognito()

    def login(self, email: str, password: str):
        try:
            return self._cognito.initiate_auth(email, password)
        except Exception as e:
            logging.warning(e)
            raise UnauthorizedError("Invalid credentials")

    def register(self, email: str, password: str):
        try:
            return self._cognito.sign_up(email, password)
        except Exception as e:
            logging.warning(e)
            raise UnauthorizedError("Invalid credentials")

    def confirm_registration(self, email: str, confirmation_code: str):
        try:
            return self._cognito.confirm_sign_up(email, confirmation_code)
        except Exception as e:
            logging.warning(e)
            raise UnauthorizedError("Invalid credentials")
