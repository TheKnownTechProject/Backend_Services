from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str = Field(min_length=8, max_length=120)
    profileImageUrl: str | None = Field(default=None, max_length=500)
    bio: str | None = Field(default=None, max_length=500)
    isActive: bool = True


class UpdateUserRequest(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    email: EmailStr
    password: str | None = Field(default=None, min_length=8, max_length=120)
    profileImageUrl: str | None = Field(default=None, max_length=500)
    bio: str | None = Field(default=None, max_length=500)
    isActive: bool = True


class UserResponse(BaseModel):
    userId: str
    username: str
    name: str
    email: EmailStr
    roleId: str
    profileImageUrl: str | None = None
    bio: str | None = None
    isActive: bool
    isSuperAdmin: bool
    createdAt: str
    modifiedAt: str


class UserListResponse(BaseModel):
    items: list[UserResponse]
