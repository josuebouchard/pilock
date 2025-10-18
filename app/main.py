from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse

# === START CREATE DB TABLES ===
from db import create_db_and_tables

from .ui.tags import router as tag_router

# Routers
from .ui.users import router as user_mgmt_router

create_db_and_tables()
# === END CREATE DB TABLES ===


# Create FastAPI main controller
app = FastAPI()

# Add routers
app.include_router(user_mgmt_router)
app.include_router(tag_router)


@app.get("/")
def home(request: Request):
    return RedirectResponse(request.url_for("users:index"))
