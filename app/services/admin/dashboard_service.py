from app.schemas.admin.dashboard_schema import DashboardSummaryResponse, DashboardTopBlogItem


class DashboardService:
    def __init__(self, blog_analytics_repository, blog_metadata_repository):
        self.blog_analytics_repository = blog_analytics_repository
        self.blog_metadata_repository = blog_metadata_repository

    def get_summary(self) -> DashboardSummaryResponse:
        analytics = self.blog_analytics_repository.list_all()
        top_blogs = self.get_top_blogs(5)
        return DashboardSummaryResponse(
            totalViews=sum(item["totalViews"] for item in analytics),
            totalLikes=sum(item["totalLikes"] for item in analytics),
            totalShares=sum(item["totalShares"] for item in analytics),
            highestViewCount=max((item["totalViews"] for item in analytics), default=0),
            topBlogs=top_blogs,
        )

    def get_top_blogs(self, limit: int) -> list[DashboardTopBlogItem]:
        items = self.blog_analytics_repository.list_all()[:limit]
        result: list[DashboardTopBlogItem] = []
        for item in items:
            blog = self.blog_metadata_repository.get_by_id(item["blogId"])
            result.append(
                DashboardTopBlogItem(
                    blogId=item["blogId"],
                    title=blog["title"] if blog else "Deleted blog",
                    totalViews=item["totalViews"],
                )
            )
        return result
