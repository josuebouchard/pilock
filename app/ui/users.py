from fastapi import APIRouter, Request, responses

from app.users.models import get_users
from db import SessionDep
from templates import templates

router = APIRouter(
    prefix="/users",
    default_response_class=responses.HTMLResponse,
)


@router.get("/", name="users:index")
def index(request: Request, session: SessionDep):
    users = get_users(session)
    return templates.TemplateResponse(
        request,
        name="user_management/index.jinja",
        context={
            "users": users,
        },
    )
