from src.shared.cognito import Cognito


class Auth:
    def __init__(self) -> None:
        self._cognito = Cognito()

    def login(self, email: str, password: str):
        response = self._cognito.initiate_auth(email, password)
        if not response:
            raise Exception("Invalid credentials")

        return response
