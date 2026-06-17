from app.repositories.db.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def get_by_email(self, email: str) -> dict | None:
        normalized = email.lower()
        for item in self.store.users.values():
            if item["email"] == normalized and not item["isDeleted"]:
                return item
        return None

    def get_by_id(self, user_id: str) -> dict | None:
        item = self.store.users.get(user_id)
        if item and not item["isDeleted"]:
            return item
        return None
