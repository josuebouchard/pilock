from fastapi import FastAPI, Request, APIRouter
from templates import templates

# === START CREATE DB TABLES ===
from db import create_db_and_tables

create_db_and_tables()
# === END CREATE DB TABLES ===


# Create FastAPI main controller
app = FastAPI()

# Tags
tag_router = APIRouter(prefix="/tags")


@tag_router.get("/", name="tags:index-ui")
def tag_index(request: Request):
    return templates.TemplateResponse(
        request,
        name="tags/index.jinja",
        context={},
    )


@tag_router.get("/create", name="tags:create-ui")
def tag_create(request: Request):
    return templates.TemplateResponse(
        request,
        name="tags/create.jinja",
        context={
            "form": {},  # optional dict to prefill (empty for new)
            "errors": {},  # optional dict for validation errors
            "csrf_token": None,
        },
    )


# Access log
logs_router = APIRouter(prefix="/logs")


@logs_router.get("/", name="logs:index-ui")
def access_log_index(request: Request):
    return templates.TemplateResponse(
        request,
        name="logs/index.jinja",
        context={},
    )


# Set routers
app.include_router(tag_router)
app.include_router(logs_router)
