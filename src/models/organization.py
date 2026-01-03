from uuid import uuid4

from dynolayer import DynoLayer

from src.shared.constants import Env


class Organization(DynoLayer):
    def __init__(self) -> None:
        super().__init__(Env.HOOK_WATCH_SINGLE_TABLE)
        self.gsi1sk = None
        self.gsi1pk = None
        self.sk = None
        self.pk = None
        self.organization_id = str(uuid4())

    def save(self):
        self.pk = f"ORG#{self.organization_id}"
        self.sk = "META"
        self.gsi1pk = "ORG"
        self.gsi1sk = f"ORG#{self.organization_id}"

        return super().save()
