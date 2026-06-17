from pydantic import BaseModel, Field


class CreateTagRequest(BaseModel):
    tagLabel: str = Field(min_length=2, max_length=120)
    slug: str | None = Field(default=None, min_length=2, max_length=160)
    categoryIds: list[str] = Field(default_factory=list)
    isActive: bool = True


class UpdateTagRequest(CreateTagRequest):
    pass


class TagResponse(BaseModel):
    tagId: str
    tagLabel: str
    slug: str
    categoryIds: list[str]
    blogCount: int
    isActive: bool
    createdAt: str
    modifiedAt: str


class TagListResponse(BaseModel):
    items: list[TagResponse]
