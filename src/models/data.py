from typing import Optional

from pydantic import BaseModel


class Data(BaseModel):
    subject: Optional[str]
    channel: str
    message: str
    datetime: str
