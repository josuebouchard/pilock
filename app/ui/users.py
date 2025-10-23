from fastapi import APIRouter, Request, responses

from app.users.models import get_users
from db import SessionDep
from templates import templates

router = APIRouter(
    prefix="/users",
    default_response_class=responses.HTMLResponse,
)


@router.get("/", name="users:index-ui")
def index(request: Request, session: SessionDep):
    users = get_users(session)
    return templates.TemplateResponse(
        request,
        name="user_management/index.jinja",
        context={
            "users": users,
        },
    )


@router.get("/create", name="users:create-ui")
def create(request: Request):
    return templates.TemplateResponse(
        request,
        name="user_management/create.jinja",
        context={
            "form": {},  # optional dict to prefill (empty for new)
            "errors": {
                "first_name": "Algo esta mal",
            },  # optional dict for validation errors
            "csrf_token": None,  # if using Flask-WTF or similar
        },
    )
