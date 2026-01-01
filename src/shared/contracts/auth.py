from dataclasses import dataclass


@dataclass
class AuthenticationResult:
    access_token: str
    id_token: str
    refresh_token: str
    expires_in: int
    token_type: str
