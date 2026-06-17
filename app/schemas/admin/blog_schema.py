from typing import Any

from pydantic import BaseModel, Field


class BlogMetadataPayload(BaseModel):
    title: str | None = Field(default=None, max_length=250)
    slug: str | None = Field(default=None, max_length=250)
    shortDescription: str | None = Field(default=None, max_length=500)
    coverImageUrl: str | None = Field(default=None, max_length=500)
    authorId: str | None = None
    categoryId: str | None = None
    tagIds: list[str] = Field(default_factory=list)
    isFeatured: bool = False
    isTrending: bool = False
    seoTitle: str | None = Field(default=None, max_length=250)
    seoDescription: str | None = Field(default=None, max_length=300)
    seoKeywords: list[str] = Field(default_factory=list)


class BlogContentPayload(BaseModel):
    contentHtml: str | None = None
    contentBlocks: list[dict[str, Any]] = Field(default_factory=list)


class CreateBlogRequest(BaseModel):
    metadata: BlogMetadataPayload
    content: BlogContentPayload
    statusAction: str = Field(pattern="^(draft|published)$")


class UpdateBlogRequest(BaseModel):
    metadata: BlogMetadataPayload
    content: BlogContentPayload


class UpdateBlogStatusRequest(BaseModel):
    status: str = Field(pattern="^(draft|published|archived|pending)$")


class BlogPreviewRequest(BaseModel):
    metadata: BlogMetadataPayload
    content: BlogContentPayload


class BlogAnalyticsSummary(BaseModel):
    totalViews: int
    totalLikes: int
    totalShares: int


class AdminBlogListItem(BaseModel):
    blogId: str
    title: str
    slug: str
    status: str
    categoryId: str | None = None
    categoryLabel: str | None = None
    publishedAt: str | None = None
    modifiedAt: str


class AdminBlogListResponse(BaseModel):
    items: list[AdminBlogListItem]


class AdminBlogDetailResponse(BaseModel):
    blogId: str
    metadata: dict[str, Any]
    content: dict[str, Any]
    analytics: BlogAnalyticsSummary


class BlogPreviewResponse(BaseModel):
    metadata: dict[str, Any]
    content: dict[str, Any]
    derived: dict[str, Any]
