class BaseError(Exception):
    def __init__(self, name: str, status_code: int, error_message: str):
        self.status_code = status_code
        self.error_message = error_message
        self.name = name

    def to_dict(self):
        return {
            "name": self.name,
            "message": self.error_message,
            "status_code": self.status_code
        }
