from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")

# For `from templates import *`
__all__ = ["templates", "HTMLResponse"]
