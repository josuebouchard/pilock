from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

templates = Jinja2Templates(directory="templates")

# For `from templates import *`
__all__ = ["templates", "HTMLResponse"]
