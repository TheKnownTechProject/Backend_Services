from app.repositories.db.base_repository import BaseRepository
from app.utils.pagination import decode_cursor, encode_cursor


class BlogAssetRepository(BaseRepository):
    def list_items(self, cursor: str | None, limit: int, asset_type: str | None = None) -> tuple[list[dict], str | None]:
        items = [item for item in self.store.blog_assets.values() if not item["isDeleted"]]
        if asset_type:
            items = [item for item in items if item["assetType"] == asset_type]
        items.sort(key=lambda item: item["createdAt"], reverse=True)
        offset = decode_cursor(cursor)
        page = items[offset : offset + limit]
        next_cursor = encode_cursor(offset + limit) if offset + limit < len(items) else None
        return page, next_cursor

    def get_by_id(self, asset_id: str) -> dict | None:
        item = self.store.blog_assets.get(asset_id)
        if item and not item["isDeleted"]:
            return item
        return None

    def save(self, item: dict) -> dict:
        self.store.blog_assets[item["assetId"]] = item
        return item

    def soft_delete(self, asset_id: str) -> None:
        self.store.blog_assets[asset_id]["isDeleted"] = True
