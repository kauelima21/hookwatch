from src.shared.contracts.base_error import BaseError


class UnauthorizedError(BaseError):
    def __init__(self, error_message: str = None):
        message = error_message if error_message else "Unauthorized error."
        super().__init__("UnauthorizedError", 401, message)
