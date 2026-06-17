from pydantic import BaseModel, Field


class CreateCategoryRequest(BaseModel):
    categoryLabel: str = Field(min_length=2, max_length=120)
    slug: str | None = Field(default=None, min_length=2, max_length=160)
    description: str | None = Field(default=None, max_length=500)
    isActive: bool = True


class UpdateCategoryRequest(CreateCategoryRequest):
    pass


class CategoryResponse(BaseModel):
    categoryId: str
    categoryLabel: str
    slug: str
    description: str | None = None
    isActive: bool
    blogCount: int
    createdAt: str
    modifiedAt: str


class CategoryListResponse(BaseModel):
    items: list[CategoryResponse]
