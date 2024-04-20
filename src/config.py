from pydantic.v1 import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    # smtp
    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    # telegram
    API_ID: int
    API_HASH: str

    # proxy
    PROXY_IP: str
    PROXY_PORT: int
    PROXY_NAME: str
    PROXY_PASS: str


settings = Settings()
