from pydantic import BaseModel, EmailStr


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class AdminUserResponse(BaseModel):
    userId: str
    name: str
    email: EmailStr
    profileImageUrl: str | None = None
    bio: str | None = None


class LoginResponse(BaseModel):
    accessToken: str
    user: AdminUserResponse
