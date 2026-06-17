from app.core.config import get_settings
from app.core.exceptions import NotFoundException, ValidationException
from app.repositories.db.blog_asset_repository import BlogAssetRepository
from app.repositories.s3.asset_storage_repository import LocalAssetStorageRepository
from app.schemas.admin.asset_schema import AssetResponse
from app.utils.datetime import utc_now_iso
from app.utils.id_generator import generate_id


class AssetService:
    def __init__(self, asset_repository: BlogAssetRepository, asset_storage_repository: LocalAssetStorageRepository):
        self.asset_repository = asset_repository
        self.asset_storage_repository = asset_storage_repository
        self.settings = get_settings()

    def list_assets(self, cursor: str | None, limit: int, asset_type: str | None = None) -> tuple[list[AssetResponse], str | None]:
        items, next_cursor = self.asset_repository.list_items(cursor, limit, asset_type)
        return [self._to_response(item) for item in items], next_cursor

    def upload_asset(
        self,
        *,
        file_name: str,
        mime_type: str,
        content: bytes,
        alt_text: str | None,
        asset_type: str,
        uploaded_by: str,
    ) -> AssetResponse:
        self._validate_upload(file_name, mime_type, content, alt_text)

        asset_id = generate_id()
        storage_result = self.asset_storage_repository.upload(asset_id, file_name, content)
        item = {
            "assetId": asset_id,
            "assetType": asset_type,
            "url": storage_result["url"],
            "fileName": file_name,
            "mimeType": mime_type,
            "altText": alt_text,
            "uploadedBy": uploaded_by,
            "createdAt": utc_now_iso(),
            "isDeleted": False,
            "s3Key": storage_result["s3Key"],
            "fileSize": len(content),
        }
        return self._to_response(self.asset_repository.save(item))

    def get_asset(self, asset_id: str) -> AssetResponse:
        item = self.asset_repository.get_by_id(asset_id)
        if not item:
            raise NotFoundException("Asset not found.")
        return self._to_response(item)

    def delete_asset(self, asset_id: str) -> None:
        item = self.asset_repository.get_by_id(asset_id)
        if not item:
            raise NotFoundException("Asset not found.")
        self.asset_repository.soft_delete(asset_id)

    def _validate_upload(self, file_name: str, mime_type: str, content: bytes, alt_text: str | None) -> None:
        if not file_name:
            raise ValidationException("File name is required.")
        if mime_type.lower() not in self.settings.allowed_file_types_set:
            raise ValidationException("File type is not allowed.")
        if len(content) > self.settings.max_file_size_mb * 1024 * 1024:
            raise ValidationException("File size exceeds the configured maximum.")
        if mime_type.lower().startswith("image/") and not alt_text:
            raise ValidationException("Alt text is required for image assets.")

    def _to_response(self, item: dict) -> AssetResponse:
        return AssetResponse(**item)
