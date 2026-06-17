from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    app_name: str = "The Tech Project Admin Backend"
    app_env: str = "development"
    api_v1_prefix: str = "/api/v1"

    aws_region: str = "ap-south-1"
    aws_access_key_id: str = "local-access-key"
    aws_secret_access_key: str = "local-secret-key"
    dynamodb_endpoint_url: str | None = None
    s3_bucket_name: str = "the-tech-project-assets"

    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 2880

    allowed_file_types: str = "image/jpeg,image/png,image/webp,image/gif"
    max_file_size_mb: int = 10
    local_asset_dir: str = "storage/assets"

    super_admin_username: str = "superadmin"
    super_admin_password: str = "Tech@1234"
    super_admin_name: str = "Super Admin"
    super_admin_email: str = "superadmin@thetechproject.local"
    data_encryption_secret: str = "change-me"

    default_page_size: int = Field(default=10, ge=1, le=100)
    max_page_size: int = Field(default=50, ge=1, le=100)

    @property
    def allowed_file_types_set(self) -> set[str]:
        return {item.strip().lower() for item in self.allowed_file_types.split(",") if item.strip()}

    @property
    def local_asset_path(self) -> Path:
        return Path(self.local_asset_dir)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.local_asset_path.mkdir(parents=True, exist_ok=True)
    return settings
