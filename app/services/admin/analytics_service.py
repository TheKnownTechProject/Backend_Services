from app.core.exceptions import NotFoundException
from app.schemas.admin.analytics_schema import (
    AnalyticsOverviewResponse,
    BlogAnalyticsDetailResponse,
    BlogMetricResponse,
)


class AnalyticsService:
    def __init__(self, blog_analytics_repository, blog_metadata_repository):
        self.blog_analytics_repository = blog_analytics_repository
        self.blog_metadata_repository = blog_metadata_repository

    def get_overview(self) -> AnalyticsOverviewResponse:
        items = self.blog_analytics_repository.list_all()
        return AnalyticsOverviewResponse(
            totalViews=sum(item["totalViews"] for item in items),
            totalLikes=sum(item["totalLikes"] for item in items),
            totalShares=sum(item["totalShares"] for item in items),
            highestViewCount=max((item["totalViews"] for item in items), default=0),
        )

    def list_blog_metrics(self) -> list[BlogMetricResponse]:
        metrics: list[BlogMetricResponse] = []
        for item in self.blog_analytics_repository.list_all():
            blog = self.blog_metadata_repository.get_by_id(item["blogId"])
            metrics.append(
                BlogMetricResponse(
                    blogId=item["blogId"],
                    title=blog["title"] if blog else "Deleted blog",
                    viewCount=item["totalViews"],
                    likeCount=item["totalLikes"],
                    shareCount=item["totalShares"],
                )
            )
        return metrics

    def get_blog_analytics(self, blog_id: str) -> BlogAnalyticsDetailResponse:
        item = self.blog_analytics_repository.get_by_blog_id(blog_id)
        if not item:
            raise NotFoundException("Analytics record not found.")
        blog = self.blog_metadata_repository.get_by_id(blog_id)
        return BlogAnalyticsDetailResponse(
            blogId=blog_id,
            title=blog["title"] if blog else "Deleted blog",
            totalViews=item["totalViews"],
            totalLikes=item["totalLikes"],
            totalShares=item["totalShares"],
            viewsByDate=item["viewsByDate"],
        )
