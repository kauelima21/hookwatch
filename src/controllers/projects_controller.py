from src.models.organization_project import OrganizationProject
from src.models.organization_user import OrganizationUser
from src.models.project import Project
from src.shared.contracts.controller import BaseController
from src.shared.http.http_request import HttpRequest
from src.shared.http.http_response import HttpResponse


class ProjectsController(BaseController):
    def __init__(self, req: HttpRequest, res: HttpResponse) -> None:
        super().__init__(req, res)

        organization_id = self.req.params["organization_id"]
        user_email = self.req.authenticated_user["email"]

        self._verify_if_user_is_member_of_organization(organization_id, user_email)

    def index(self) -> dict:
        last_key = self.req.query.get("last_key")
        per_page = self.req.query.get("per_page", 10)

        organization_id = self.req.params["organization_id"]

        projects_query = (
            OrganizationProject()
            .where("pk", f"ORG#{organization_id}")
            .and_where("sk", "begins_with", "PROJECT#")
            .limit(per_page)
            .offset(last_key)
        )
        organization_projects = projects_query.fetch()

        return self.res.json({
            "data": organization_projects.to_list(),
            "per_page": per_page,
            "count": projects_query.get_count(),
            "last_key": projects_query.last_evaluated_key()
        })

    def show(self) -> dict:
        project_id = self.req.params["project_id"]

        project = (
            Project()
            .find_or_fail({"pk": f"PROJECT#{project_id}", "sk": "META"})
        )

        return self.res.json(project.data())

    def store(self) -> dict:
        organization_id = self.req.params["organization_id"]

        project = Project()
        project.organization_id = organization_id
        project.name = self.req.body["name"]
        project.description = self.req.body["description"]
        project.target_url = self.req.body["target_url"]
        project.api_key = self.req.body["api_key"]

        project.save()

        organization_project = OrganizationProject()
        organization_project.project_id = project.project_id
        organization_project.organization_id = organization_id

        organization_project.save()

        return self.res.status(201).json({"message": project.project_id})

    def _verify_if_user_is_member_of_organization(self, organization_id: str, user_email: str) -> bool:
        is_user_part_of_organization = (
            OrganizationUser()
            .where("pk", f"ORG#{organization_id}")
            .and_where("sk", f"USER#{user_email}")
            .fetch(return_all=True)
        )

        if not is_user_part_of_organization:
            return self.res.status(403).json({"message": "You are not part of this organization"})

        return True
