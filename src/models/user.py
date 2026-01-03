from dynolayer import DynoLayer

from src.shared.constants import Env


class User(DynoLayer):
    def __init__(self) -> None:
        super().__init__(Env.HOOK_WATCH_SINGLE_TABLE, required_fields=["email", "system_role", "status"])
        self.gsi1sk = None
        self.gsi1pk = None
        self.sk = None
        self.pk = None

    def find_by_email(self, email: str):
        return self.find({"pk": f"USER#{email}", "sk": "META"})

    def save(self):
        self.pk = f"USER#{self.email}"
        self.sk = "META"
        self.gsi1pk = "USER"
        self.gsi1sk = f"USER#{self.email}"

        return super().save()
