import os
from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = Field(..., env="localhost:5432")
    instagram_access_token: str = Field(..., env="INSTAGRAM_ACCESS_TOKEN")
    instagram_user_id: str = Field(..., env="INSTAGRAM_USER_ID")
    telegram_bot_token: str = Field(..., env="TELEGRAM_BOT_TOKEN")
    telegram_chat_id: str = Field(..., env="TELEGRAM_CHAT_ID")
    basic_auth_username: str = Field("admin", env="BASIC_AUTH_USERNAME")
    basic_auth_password: str = Field("admin", env="BASIC_AUTH_PASSWORD")
    milestone_threshold: int = Field(1000, env="MILESTONE_THRESHOLD")
    mock: bool = Field(False, env="MOCK")

    class Config:
        env_file = ".env"


settings = Settings()
