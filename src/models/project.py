from uuid import uuid4

from dynolayer import DynoLayer

from src.shared.constants import Env


class Project(DynoLayer):
    def __init__(self) -> None:
        super().__init__(Env.HOOK_WATCH_SINGLE_TABLE)

        self.gsi1sk = None
        self.gsi1pk = None
        self.sk = None
        self.pk = None
        self.project_id = str(uuid4())
        self.type = "PROJECT"

    def save(self):
        self.pk = f"PROJECT#{self.project_id}"
        self.sk = "META"
        self.gsi1pk = "PROJECT"
        self.gsi1sk = f"PROJECT#{self.project_id}"

        return super().save()
