from app.core.exceptions import UnauthorizedException
from app.core.security import create_access_token, decode_access_token, verify_password
from app.repositories.db.user_repository import UserRepository
from app.schemas.admin.auth_schema import AdminUserResponse, LoginResponse


class AuthService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, email: str, password: str) -> LoginResponse:
        user = self.user_repository.get_by_email(email)
        if not user or not user["isActive"]:
            raise UnauthorizedException("Invalid email or password.")
        if not verify_password(password, user["passwordHash"]):
            raise UnauthorizedException("Invalid email or password.")

        token = create_access_token(user["userId"])
        user_response = self._build_user_response(user)
        return LoginResponse(accessToken=token, user=user_response)

    def get_user_from_token(self, token: str) -> dict:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if not user_id:
            raise UnauthorizedException("Invalid access token.")
        user = self.user_repository.get_by_id(user_id)
        if not user or not user["isActive"]:
            raise UnauthorizedException("User is inactive or missing.")
        return {
            "userId": user["userId"],
            "name": user["name"],
            "email": user["email"],
            "profileImageUrl": user["profileImageUrl"],
            "bio": user["bio"],
        }

    def get_login_user_details(self, user: dict) -> AdminUserResponse:
        return AdminUserResponse(**user)

    def raise_unauthorized(self) -> None:
        raise UnauthorizedException("Authentication is required.")

    def _build_user_response(self, user: dict) -> AdminUserResponse:
        return AdminUserResponse(
            userId=user["userId"],
            name=user["name"],
            email=user["email"],
            profileImageUrl=user["profileImageUrl"],
            bio=user["bio"],
        )
