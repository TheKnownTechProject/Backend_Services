from app.repositories.db.base_repository import BaseRepository
from app.utils.pagination import decode_cursor, encode_cursor


class BlogMetadataRepository(BaseRepository):
    def list_items(
        self,
        cursor: str | None,
        limit: int,
        status: str | None = None,
        search: str | None = None,
        category_id: str | None = None,
    ) -> tuple[list[dict], str | None]:
        items = [item for item in self.store.blogs_metadata.values() if not item["isDeleted"]]
        if status:
            items = [item for item in items if item["blogStatus"] == status]
        if category_id:
            items = [item for item in items if item["categoryId"] == category_id]
        if search:
            needle = search.lower()
            items = [item for item in items if needle in item["title"].lower() or needle in item["slug"].lower()]

        items.sort(key=lambda item: item["modifiedAt"], reverse=True)
        offset = decode_cursor(cursor)
        page = items[offset : offset + limit]
        next_cursor = encode_cursor(offset + limit) if offset + limit < len(items) else None
        return page, next_cursor

    def list_all(self) -> list[dict]:
        items = [item for item in self.store.blogs_metadata.values() if not item["isDeleted"]]
        return sorted(items, key=lambda item: item["modifiedAt"], reverse=True)

    def get_by_id(self, blog_id: str) -> dict | None:
        item = self.store.blogs_metadata.get(blog_id)
        if item and not item["isDeleted"]:
            return item
        return None

    def get_by_slug(self, slug: str, exclude_blog_id: str | None = None) -> dict | None:
        for item in self.store.blogs_metadata.values():
            if item["isDeleted"]:
                continue
            if item["slug"] == slug and item["blogId"] != exclude_blog_id:
                return item
        return None

    def save(self, item: dict) -> dict:
        self.store.blogs_metadata[item["blogId"]] = item
        return item

    def soft_delete(self, blog_id: str) -> None:
        self.store.blogs_metadata[blog_id]["isDeleted"] = True

    def count_by_category_id(self, category_id: str) -> int:
        return len(
            [
                item
                for item in self.store.blogs_metadata.values()
                if not item["isDeleted"] and item["categoryId"] == category_id
            ]
        )

    def count_by_tag_id(self, tag_id: str) -> int:
        return len(
            [item for item in self.store.blogs_metadata.values() if not item["isDeleted"] and tag_id in item["tagIds"]]
        )
