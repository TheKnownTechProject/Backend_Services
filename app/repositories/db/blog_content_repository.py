from app.repositories.db.base_repository import BaseRepository


class BlogContentRepository(BaseRepository):
    def get_by_blog_id(self, blog_id: str) -> dict | None:
        item = self.store.blogs_contents.get(blog_id)
        if item and not item["isDeleted"]:
            return item
        return None

    def save(self, item: dict) -> dict:
        self.store.blogs_contents[item["blogId"]] = item
        return item

    def soft_delete(self, blog_id: str) -> None:
        if blog_id in self.store.blogs_contents:
            self.store.blogs_contents[blog_id]["isDeleted"] = True
