from app.core.security import decrypt_text
from app.repositories.db.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def get_by_id(self, user_id: str) -> dict | None:
        item = self.store.users.get(user_id)
        if item and not item["isDeleted"]:
            return item
        return None

    def list_all(self) -> list[dict]:
        items = [item for item in self.store.users.values() if not item["isDeleted"]]
        return sorted(items, key=lambda item: item["modifiedAt"], reverse=True)

    def get_super_admin(self) -> dict | None:
        for item in self.store.users.values():
            if item.get("isSuperAdmin") and not item["isDeleted"]:
                return item
        return None

    def find_by_login_username(self, username: str) -> dict | None:
        normalized = username.strip().lower()
        for item in self.store.users.values():
            if item["isDeleted"] or item.get("isSuperAdmin"):
                continue
            if decrypt_text(item["email"]) == normalized:
                return item
        return None

    def exists_by_email(self, email: str, exclude_user_id: str | None = None) -> bool:
        normalized = email.strip().lower()
        for item in self.store.users.values():
            if item["isDeleted"] or item["userId"] == exclude_user_id:
                continue
            item_email = item["email"] if item.get("isSuperAdmin") else decrypt_text(item["email"])
            if item_email == normalized:
                return True
        return False

    def save(self, item: dict) -> dict:
        self.store.users[item["userId"]] = item
        return item

    def soft_delete(self, user_id: str) -> None:
        self.store.users[user_id]["isDeleted"] = True
