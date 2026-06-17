from app.repositories.db.base_repository import BaseRepository


class BlogAnalyticsRepository(BaseRepository):
    def get_by_blog_id(self, blog_id: str) -> dict | None:
        item = self.store.blog_analytics.get(blog_id)
        if item and not item["isDeleted"]:
            return item
        return None

    def save(self, item: dict) -> dict:
        self.store.blog_analytics[item["blogId"]] = item
        return item

    def list_all(self) -> list[dict]:
        items = [item for item in self.store.blog_analytics.values() if not item["isDeleted"]]
        return sorted(items, key=lambda item: item["totalViews"], reverse=True)
