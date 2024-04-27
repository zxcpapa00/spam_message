from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from src.db.db import database

router = APIRouter(prefix="")

templates = Jinja2Templates(directory="src/templates")


@router.get("/")
def get_index_page(request: Request):
    user = database.get(request.client.host)
    if not user:
        database[request.client.host] = {}
    return templates.TemplateResponse("index.html", {"request": request})


@router.get("/data")
def reset_data(request: Request):
    user_data = database.get(request.client.host)
    user_email = "default"
    user_telegram = "default"
    if user_data.get("email"):
        user_email = user_data.get("email")
    if user_data.get("telegram"):
        user_telegram = user_data.get("telegram")

    return templates.TemplateResponse("reset_data.html",
                                      {"request": request, "user_email": user_email, "user_telegram": user_telegram}
                                      )
