from pathlib import Path
from urllib.parse import quote

from app.core.config import get_settings


class LocalAssetStorageRepository:
    def __init__(self) -> None:
        self.settings = get_settings()

    def upload(self, asset_id: str, file_name: str, content: bytes) -> dict[str, str]:
        safe_name = Path(file_name).name
        now_path = Path(self.settings.local_asset_dir) / "blog-assets"
        now_path.mkdir(parents=True, exist_ok=True)
        storage_path = now_path / f"{asset_id}-{safe_name}"
        storage_path.write_bytes(content)
        return {
            "url": f"/local-assets/blog-assets/{quote(storage_path.name)}",
            "s3Key": f"blog-assets/{storage_path.name}",
        }
