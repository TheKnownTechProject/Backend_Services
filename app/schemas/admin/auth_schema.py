from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    username: str
    password: str


class AdminUserResponse(BaseModel):
    userId: str
    username: str
    name: str
    email: EmailStr
    roleId: str
    isSuperAdmin: bool
    profileImageUrl: str | None = None
    bio: str | None = None


class LoginResponse(BaseModel):
    accessToken: str
    user: AdminUserResponse
