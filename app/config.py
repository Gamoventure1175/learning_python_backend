from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expires_minutes: int

    model_config = SettingsConfigDict(env_file="./.env")


settings = Settings()  # type: ignore