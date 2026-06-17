from app.core.config import get_settings
from app.core.exceptions import UnauthorizedException
from app.core.security import decrypt_text
from app.core.security import create_access_token, decode_access_token, verify_password
from app.repositories.db.user_repository import UserRepository
from app.schemas.admin.auth_schema import AdminUserResponse, LoginResponse

FALLBACK_SUPER_ADMIN_ID = "fallback-super-admin"


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository
        self.settings = get_settings()

    def login(self, username: str, password: str) -> LoginResponse:
        normalized_username = username.strip().lower()
        user = self._authenticate_super_admin(normalized_username, password)
        if not user:
            user = self.user_repository.find_by_login_username(normalized_username)
            if not user or not user["isActive"]:
                raise UnauthorizedException("Invalid username or password.")
            if not verify_password(password, user["password"]):
                raise UnauthorizedException("Invalid username or password.")

        token = create_access_token(user["userId"])
        user_response = self._build_user_response(user)
        return LoginResponse(accessToken=token, user=user_response)

    def get_user_from_token(self, token: str) -> dict:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid access token.")
        if user_id == FALLBACK_SUPER_ADMIN_ID:
            return self._serialize_user(self._build_fallback_super_admin())
        user = self.user_repository.get_by_id(user_id)
        if not user or not user["isActive"]:
            raise UnauthorizedException("User is inactive or missing.")
        return self._serialize_user(user)

    def get_login_user_details(self, user: dict) -> AdminUserResponse:
        return AdminUserResponse(**user)

    def raise_unauthorized(self) -> None:
        raise UnauthorizedException("Authentication is required.")

    def _build_user_response(self, user: dict) -> AdminUserResponse:
        return AdminUserResponse(
            **self._serialize_user(user),
        )

    def _authenticate_super_admin(self, username: str, password: str) -> dict | None:
        if username != self.settings.super_admin_username.lower():
            return None

        stored_super_admin = self.user_repository.get_super_admin()
        if stored_super_admin:
            if not stored_super_admin["isActive"] or stored_super_admin["isDeleted"]:
                raise UnauthorizedException("Super admin account is inactive.")
            if stored_super_admin["password"] != password:
                raise UnauthorizedException("Invalid username or password.")
            return stored_super_admin

        if password != self.settings.super_admin_password:
            raise UnauthorizedException("Invalid username or password.")
        return self._build_fallback_super_admin()

    def _build_fallback_super_admin(self) -> dict:
        return {
            "userId": FALLBACK_SUPER_ADMIN_ID,
            "username": self.settings.super_admin_username,
            "name": self.settings.super_admin_name,
            "email": self.settings.super_admin_email.lower(),
            "roleId": "admin",
            "profileImageUrl": None,
            "bio": None,
            "isActive": True,
            "isSuperAdmin": True,
            "createdAt": "2026-06-17T00:00:00Z",
            "modifiedAt": "2026-06-17T00:00:00Z",
            "isDeleted": False,
        }

    def _serialize_user(self, user: dict) -> dict:
        email = user["email"] if user.get("isSuperAdmin") else decrypt_text(user["email"])
        return {
            "userId": user["userId"],
            "username": user.get("username") or email,
            "name": user["name"],
            "email": email,
            "roleId": user.get("roleId", "admin"),
            "isSuperAdmin": user.get("isSuperAdmin", False),
            "profileImageUrl": user.get("profileImageUrl"),
            "bio": user.get("bio"),
        }
