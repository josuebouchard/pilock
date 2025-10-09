from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse

# Routers
from .ui.users import router as user_mgmt_router
from .ui.tags import router as tag_router

# === START CREATE DB TABLES ===
from .users.tables import UserModel
from db import create_db_and_tables

create_db_and_tables()
# === END CREATE DB TABLES ===


# Create FastAPI main controller
app = FastAPI()

# Add routers
app.include_router(user_mgmt_router)
app.include_router(tag_router)

# Static files
app.mount("/static", StaticFiles(directory="./static"), name="static")


@app.get("/")
def home(request: Request):
    return RedirectResponse(request.url_for("users:index"))
