from pydantic import BaseModel


class DashboardTopBlogItem(BaseModel):
    blogId: str
    title: str
    totalViews: int


class DashboardSummaryResponse(BaseModel):
    totalViews: int
    totalLikes: int
    totalShares: int
    highestViewCount: int
    topBlogs: list[DashboardTopBlogItem]
