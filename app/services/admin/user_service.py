from app.core.exceptions import ConflictException, NotFoundException, ValidationException
from app.core.security import decrypt_text, encrypt_text, hash_password
from app.repositories.db.user_repository import UserRepository
from app.schemas.admin.user_schema import CreateUserRequest, UpdateUserRequest, UserResponse
from app.utils.datetime import utc_now_iso
from app.utils.id_generator import generate_id


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def list_users(self) -> list[UserResponse]:
        return [self._to_response(item) for item in self.user_repository.list_all()]

    def get_user(self, user_id: str) -> UserResponse:
        item = self.user_repository.get_by_id(user_id)
        if not item:
            raise NotFoundException("User not found.")
        return self._to_response(item)

    def create_user(self, payload: CreateUserRequest) -> UserResponse:
        normalized_email = payload.email.lower()
        if self.user_repository.exists_by_email(normalized_email):
            raise ConflictException("User email already exists.")

        timestamp = utc_now_iso()
        item = {
            "userId": generate_id(),
            "username": normalized_email,
            "name": payload.name.strip(),
            "email": encrypt_text(normalized_email),
            "password": hash_password(payload.password),
            "roleId": "admin",
            "profileImageUrl": payload.profileImageUrl,
            "bio": payload.bio,
            "isActive": payload.isActive,
            "isSuperAdmin": False,
            "createdAt": timestamp,
            "modifiedAt": timestamp,
            "isDeleted": False,
        }
        return self._to_response(self.user_repository.save(item))

    def update_user(self, user_id: str, payload: UpdateUserRequest) -> UserResponse:
        existing = self.user_repository.get_by_id(user_id)
        if not existing:
            raise NotFoundException("User not found.")
        if existing.get("isSuperAdmin"):
            raise ValidationException("Super admin cannot be edited from the user management APIs.")

        normalized_email = payload.email.lower()
        if self.user_repository.exists_by_email(normalized_email, exclude_user_id=user_id):
            raise ConflictException("User email already exists.")

        existing.update(
            {
                "username": normalized_email,
                "name": payload.name.strip(),
                "email": encrypt_text(normalized_email),
                "profileImageUrl": payload.profileImageUrl,
                "bio": payload.bio,
                "isActive": payload.isActive,
                "modifiedAt": utc_now_iso(),
            }
        )
        if payload.password:
            existing["password"] = hash_password(payload.password)
        return self._to_response(self.user_repository.save(existing))

    def delete_user(self, user_id: str) -> None:
        existing = self.user_repository.get_by_id(user_id)
        if not existing:
            raise NotFoundException("User not found.")
        if existing.get("isSuperAdmin"):
            raise ValidationException("Super admin cannot be deleted.")
        self.user_repository.soft_delete(user_id)

    def _to_response(self, item: dict) -> UserResponse:
        email = item["email"] if item.get("isSuperAdmin") else decrypt_text(item["email"])
        username = item.get("username") or email
        return UserResponse(
            userId=item["userId"],
            username=username,
            name=item["name"],
            email=email,
            roleId=item.get("roleId", "admin"),
            profileImageUrl=item.get("profileImageUrl"),
            bio=item.get("bio"),
            isActive=item["isActive"],
            isSuperAdmin=item.get("isSuperAdmin", False),
            createdAt=item["createdAt"],
            modifiedAt=item["modifiedAt"],
        )
