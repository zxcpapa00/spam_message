from fastapi import FastAPI

from src.pages.router import router as page_router
from src.services.receiver import router as receiver_router

app = FastAPI()
app.include_router(page_router)
app.include_router(receiver_router)
