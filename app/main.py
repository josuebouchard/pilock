from typing import Annotated
from fastapi import FastAPI, Form, Request, APIRouter, status
from fastapi.responses import RedirectResponse
from templates import templates

# === START CREATE DB TABLES ===
from db import SessionDep, create_db_and_tables
from .models import Tag, AccessLog, TagEdit  # pyright: ignore[reportUnusedImport]  # noqa: F401
from .repository import disable_tag, get_access_logs, get_tags, save_tag
from app import repository

create_db_and_tables()
# === END CREATE DB TABLES ===


# Create FastAPI main controller
app = FastAPI()


@app.get("/")
def index(request: Request):
    return RedirectResponse(request.url_for("tags:index-ui"))


# Tags
tag_router = APIRouter(prefix="/tags")

test_tags = [
    {
        "org_id": "V12345678",
        "first_name": "Richard",
        "last_name": "Magnuson",
        "tag_id": "6bd29c694c",
    },
    {
        "org_id": "V98765432",
        "first_name": "Maria",
        "last_name": "Lopez",
        "tag_id": "1fa45e72b3",
    },
    {
        "org_id": "V13579246",
        "first_name": "James",
        "last_name": "Chen",
        "tag_id": "9c3e11a9d8",
    },
    {
        "org_id": "V24681357",
        "first_name": "Sofia",
        "last_name": "Martinez",
        "tag_id": "45de77c112",
    },
    {
        "org_id": "V55588833",
        "first_name": "Omar",
        "last_name": "Hassan",
        "tag_id": "a7c29e4f90",
    },
    {
        "org_id": "V11223344",
        "first_name": "Liam",
        "last_name": "Nguyen",
        "tag_id": "0b92cd3aef",
    },
    {
        "org_id": "V99887766",
        "first_name": "Chloe",
        "last_name": "Bennett",
        "tag_id": "d23af64b9e",
    },
    {
        "org_id": "V44332211",
        "first_name": "Noah",
        "last_name": "Khan",
        "tag_id": "8ac59e20c4",
    },
]


@tag_router.get("/", name="tags:index-ui")
def tag_index_ui(request: Request, session: SessionDep):
    tags = get_tags(session)
    return templates.TemplateResponse(
        request,
        name="tags/index.jinja",
        context={"tags": tags},
    )


@tag_router.post("/create", name="tags:create")
def tag_create(
    request: Request,
    tag_edit: Annotated[TagEdit, Form()],
    session: SessionDep,
):
    tag = Tag.model_validate(tag_edit, update={"id": None})
    tag = save_tag(tag, session)

    return RedirectResponse(
        request.url_for("tags:edit", tag_id=tag.id),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@tag_router.get("/create", name="tags:create-ui")
def tag_create_ui(request: Request):
    return templates.TemplateResponse(
        request,
        name="tags/create.jinja",
        context={
            "form": {},  # optional dict to prefill (empty for new)
            "errors": {},  # optional dict for validation errors
            "csrf_token": None,
        },
    )


@tag_router.post("/{tag_id}", name="tags:edit")
def tag_edit(
    request: Request,
    tag_id: int,
    tag_edit: Annotated[TagEdit, Form()],
    session: SessionDep,
):
    tag = Tag.model_validate(tag_edit, update={"id": tag_id})
    tag = save_tag(tag, session)

    return templates.TemplateResponse(
        request,
        name="tags/edit.jinja",
        context={"form": tag.model_dump()},
    )


@tag_router.post("/{tag_id}/delete", name="tags:delete")
def tag_delete(
    request: Request,
    tag_id: int,
    session: SessionDep,
):
    disable_tag(tag_id, session)
    return RedirectResponse(
        url=request.url_for("tags:index-ui"),
        status_code=status.HTTP_303_SEE_OTHER,
    )


@tag_router.get("/{tag_id}", name="tags:edit-ui")
def tag_edit_ui(request: Request, tag_id: int, session: SessionDep):
    tag = repository.get_tag_by_id(tag_id, session)
    if tag is None:
        # TODO: do something
        return RedirectResponse(request.url_for("tags:index-ui"))

    return templates.TemplateResponse(
        request,
        name="tags/edit.jinja",
        context={"form": tag.model_dump()},
    )


# Access log
logs_router = APIRouter(prefix="/logs")


@logs_router.get("/download", name="logs:download-ui")
def access_log_download(request: Request):
    return templates.TemplateResponse(
        request,
        name="logs/download.jinja",
        context={},
    )


test_logs = [
    {
        "org_id": "V98765432",
        "first_name": "Maria",
        "last_name": "Lopez",
        "timestamp": "2025-10-31 12:10:42",
        "tag_id": "1fa45e72b3",
    },
    {
        "org_id": "V12345678",
        "first_name": "Richard",
        "last_name": "Magnuson",
        "timestamp": "2025-10-31 12:05:17",
        "tag_id": "6bd29c694c",
    },
    {
        "org_id": "V44332211",
        "first_name": "Noah",
        "last_name": "Khan",
        "timestamp": "2025-10-31 11:55:33",
        "tag_id": "8ac59e20c4",
    },
    {
        "org_id": "V98765432",
        "first_name": "Maria",
        "last_name": "Lopez",
        "timestamp": "2025-10-31 11:32:08",
        "tag_id": "1fa45e72b3",
    },
    {
        "org_id": "V99887766",
        "first_name": "Chloe",
        "last_name": "Bennett",
        "timestamp": "2025-10-31 11:10:35",
        "tag_id": "d23af64b9e",
    },
    {
        "org_id": "V12345678",
        "first_name": "Richard",
        "last_name": "Magnuson",
        "timestamp": "2025-10-31 10:55:02",
        "tag_id": "6bd29c694c",
    },
    {
        "org_id": "V55588833",
        "first_name": "Omar",
        "last_name": "Hassan",
        "timestamp": "2025-10-31 10:42:59",
        "tag_id": "a7c29e4f90",
    },
    {
        "org_id": "V24681357",
        "first_name": "Sofia",
        "last_name": "Martinez",
        "timestamp": "2025-10-31 10:15:22",
        "tag_id": "45de77c112",
    },
    {
        "org_id": "V13579246",
        "first_name": "James",
        "last_name": "Chen",
        "timestamp": "2025-10-31 10:02:47",
        "tag_id": "9c3e11a9d8",
    },
    {
        "org_id": "V12345678",
        "first_name": "Richard",
        "last_name": "Magnuson",
        "timestamp": "2025-10-31 09:23:12",
        "tag_id": "6bd29c694c",
    },
]


@logs_router.get("/", name="logs:index-ui")
def access_log_index(request: Request, session: SessionDep):
    logs = get_access_logs(session)
    return templates.TemplateResponse(
        request,
        name="logs/index.jinja",
        context={"logs": logs},
    )


# Set routers
app.include_router(tag_router)
app.include_router(logs_router)
