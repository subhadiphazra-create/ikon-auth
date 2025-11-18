from pydantic_settings import BaseSettings
from pydantic import Field
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    base_issuer_url: str = Field(...)
    oauth_client_id: str = Field(...)
    oauth_client_secret: str = Field(...)

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()
