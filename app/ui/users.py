from fastapi import APIRouter, Request, responses
from app.users.dependencies import UserRepositoryDep
from templates import templates

router = APIRouter(
    prefix="/users",
    default_response_class=responses.HTMLResponse,
)


@router.get("/", name="users:index")
def index(request: Request, user_repository: UserRepositoryDep):
    users = user_repository.get_users()
    return templates.TemplateResponse(
        request,
        name="user_management/index.jinja",
        context={
            "users": users,
        },
    )
