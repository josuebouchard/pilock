from fastapi import APIRouter, Request, responses

from templates import templates

router = APIRouter(
    prefix="/tags",
    default_response_class=responses.HTMLResponse,
)


@router.get("/", name="tags:index")
def index(request: Request):
    return templates.TemplateResponse(
        request,
        name="tags/index.jinja",
        context={},
    )
