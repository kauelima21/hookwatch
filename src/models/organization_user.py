from dynolayer import DynoLayer

from src.shared.constants import Env


class OrganizationUser(DynoLayer):
    def __init__(self) -> None:
        super().__init__(Env.HOOK_WATCH_SINGLE_TABLE)

        self.gsi2sk = None
        self.gsi2pk = None
        self.sk = None
        self.pk = None
        self.type = "ORGANIZATION_USER"

    def save(self):
        self.pk = f"ORG#{self.organization_id}"
        self.sk = f"USER#{self.user}"
        self.gsi2pk = f"USER#{self.user}"
        self.gsi2sk = f"ORG#{self.organization_id}"

        return super().save()
