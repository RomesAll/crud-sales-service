from pydantic_settings import BaseSettings, SettingsConfigDict

class PostgresConfig(BaseSettings):
    model_config = SettingsConfigDict(
        pre
    )

class Config:
    pass

config = Config()