from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Einzelne DB-Variablen aus .env
    db_password: str = "changeme"
    postgres_db: str = "vagabond"
    postgres_user: str = "vagabond"

    redis_url: str = "redis://localhost:6379/0"
    graphhopper_url: str = "http://localhost:8989"
    api_key: str = "dev-key"
    auth_mode: str = "apikey"

    model_config = {"env_file": "../.env"}

    @property
    def database_url(self) -> str:
        """Baut die DB-URL aus den Einzelteilen zusammen."""
        return f"postgresql+asyncpg://{self.postgres_user}:{self.db_password}@localhost:5432/{self.postgres_db}"


settings = Settings()