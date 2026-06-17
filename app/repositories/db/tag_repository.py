from app.repositories.db.base_repository import BaseRepository


class TagRepository(BaseRepository):
    def list_all(self) -> list[dict]:
        items = [item for item in self.store.tags.values() if not item["isDeleted"]]
        return sorted(items, key=lambda item: item["modifiedAt"], reverse=True)

    def get_by_id(self, tag_id: str) -> dict | None:
        item = self.store.tags.get(tag_id)
        if item and not item["isDeleted"]:
            return item
        return None

    def get_by_ids(self, tag_ids: list[str]) -> list[dict]:
        return [item for tag_id in tag_ids if (item := self.get_by_id(tag_id))]

    def get_by_slug(self, slug: str, exclude_tag_id: str | None = None) -> dict | None:
        for item in self.store.tags.values():
            if item["isDeleted"]:
                continue
            if item["slug"] == slug and item["tagId"] != exclude_tag_id:
                return item
        return None

    def save(self, item: dict) -> dict:
        self.store.tags[item["tagId"]] = item
        return item

    def soft_delete(self, tag_id: str) -> None:
        self.store.tags[tag_id]["isDeleted"] = True
