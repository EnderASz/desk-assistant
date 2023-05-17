from pydantic import BaseSettings


class AppConfig(BaseSettings):
    class Config:
        allow_mutation = False
