from app.repositories.db.base_repository import BaseRepository


class BlogStatusRepository(BaseRepository):
    def list_all(self) -> list[dict]:
        return [item for item in self.store.blog_statuses.values() if item["isActive"]]

    def get_by_id(self, status_id: str) -> dict | None:
        return self.store.blog_statuses.get(status_id)
