from pydantic import BaseModel


class AnalyticsOverviewResponse(BaseModel):
    totalViews: int
    totalLikes: int
    totalShares: int
    highestViewCount: int


class BlogMetricResponse(BaseModel):
    blogId: str
    title: str
    viewCount: int
    likeCount: int
    shareCount: int


class BlogMetricListResponse(BaseModel):
    items: list[BlogMetricResponse]


class BlogAnalyticsDetailResponse(BaseModel):
    blogId: str
    title: str
    totalViews: int
    totalLikes: int
    totalShares: int
    viewsByDate: dict[str, int]
