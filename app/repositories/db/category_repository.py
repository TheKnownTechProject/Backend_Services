from app.repositories.db.base_repository import BaseRepository


class CategoryRepository(BaseRepository):
    def list_all(self) -> list[dict]:
        items = [item for item in self.store.categories.values() if not item["isDeleted"]]
        return sorted(items, key=lambda item: item["modifiedAt"], reverse=True)

    def get_by_id(self, category_id: str) -> dict | None:
        item = self.store.categories.get(category_id)
        if item and not item["isDeleted"]:
            return item
        return None

    def get_by_slug(self, slug: str, exclude_category_id: str | None = None) -> dict | None:
        for item in self.store.categories.values():
            if item["isDeleted"]:
                continue
            if item["slug"] == slug and item["categoryId"] != exclude_category_id:
                return item
        return None

    def save(self, item: dict) -> dict:
        self.store.categories[item["categoryId"]] = item
        return item

    def soft_delete(self, category_id: str) -> None:
        self.store.categories[category_id]["isDeleted"] = True
