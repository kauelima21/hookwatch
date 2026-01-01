from dynolayer import DynoLayer

from src.shared.constants import Env


class User(DynoLayer):
    def __init__(self) -> None:
        super().__init__(Env.HOOK_WATCH_SINGLE_TABLE)

    def find_by_email(self, email: str):
        return self.find({"pk": f"USER#{email}", "sk": "META"})
