from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter(prefix="")

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
def get_index_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
