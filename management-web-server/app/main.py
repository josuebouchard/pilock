from datetime import datetime
from typing import Annotated
from fastapi import FastAPI, Form, Request, APIRouter, status, Response
from fastapi.responses import RedirectResponse
from templates import templates
import csv
import io

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
def access_log_download_ui(
    request: Request,
):
    return templates.TemplateResponse(
        request,
        name="logs/download.jinja",
        context={},
    )


@logs_router.post("/download", name="logs:download")
def access_log_download(
    from_date: Annotated[datetime, Form()],
    to_date: Annotated[datetime, Form()],
    session: SessionDep,
):
    access_logs = get_access_logs(
        session,
        from_datetime=from_date,
        to_datetime=to_date,
    )
    # Build CSV in memory
    buffer = io.StringIO()
    writer = csv.writer(buffer)

    # CSV Header
    writer.writerow(
        [
            "id",
            "tag_uid",
            "access_was_granted",
            "timestamp",
            "org_id",
            "first_name",
            "last_name",
        ]
    )

    # CSV Rows
    for log in access_logs:
        writer.writerow(
            [
                log.id,
                log.tag_uid,
                log.access_was_granted,
                log.timestamp.isoformat() if log.timestamp else "",
                log.org_id or "",
                log.first_name or "",
                log.last_name or "",
            ]
        )

    # Retrieve CSV string
    csv_text = buffer.getvalue()
    buffer.close()

    # Return file as CSV download
    return Response(
        content=csv_text,
        media_type="text/csv",
        headers={"Content-Disposition": 'attachment; filename="access_logs.csv"'},
    )


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
