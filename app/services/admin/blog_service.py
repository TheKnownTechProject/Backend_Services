from app.core.constants import DRAFT_STATUS_ID, PUBLISHED_STATUS_ID
from app.core.exceptions import ConflictException, NotFoundException, ValidationException
from app.repositories.db.blog_analytics_repository import BlogAnalyticsRepository
from app.repositories.db.blog_content_repository import BlogContentRepository
from app.repositories.db.blog_metadata_repository import BlogMetadataRepository
from app.repositories.db.blog_status_repository import BlogStatusRepository
from app.repositories.db.category_repository import CategoryRepository
from app.repositories.db.tag_repository import TagRepository
from app.schemas.admin.blog_schema import (
    AdminBlogDetailResponse,
    AdminBlogListItem,
    BlogAnalyticsSummary,
    BlogPreviewResponse,
    CreateBlogRequest,
    UpdateBlogRequest,
)
from app.utils.datetime import utc_now_iso
from app.utils.html_sanitizer import sanitize_html
from app.utils.id_generator import generate_id
from app.utils.reading_time import calculate_reading_time
from app.utils.slug import slugify


class BlogService:
    def __init__(
        self,
        blog_metadata_repository: BlogMetadataRepository,
        blog_content_repository: BlogContentRepository,
        blog_analytics_repository: BlogAnalyticsRepository,
        category_repository: CategoryRepository,
        tag_repository: TagRepository,
        blog_status_repository: BlogStatusRepository,
    ):
        self.blog_metadata_repository = blog_metadata_repository
        self.blog_content_repository = blog_content_repository
        self.blog_analytics_repository = blog_analytics_repository
        self.category_repository = category_repository
        self.tag_repository = tag_repository
        self.blog_status_repository = blog_status_repository

    def list_blogs(
        self,
        cursor: str | None,
        limit: int,
        status: str | None = None,
        search: str | None = None,
        category_id: str | None = None,
    ) -> tuple[list[AdminBlogListItem], str | None]:
        items, next_cursor = self.blog_metadata_repository.list_items(cursor, limit, status, search, category_id)
        return [self._to_list_item(item) for item in items], next_cursor

    def create_blog(self, payload: CreateBlogRequest, current_user: dict) -> AdminBlogDetailResponse:
        self._validate_payload(payload.metadata.categoryId, payload.metadata.tagIds)

        slug = slugify(payload.metadata.slug or payload.metadata.title or "")
        if not slug:
            raise ValidationException("Slug or title is required.")
        if self.blog_metadata_repository.get_by_slug(slug):
            raise ConflictException("Blog slug already exists.")

        status = payload.statusAction
        if not self.blog_status_repository.get_by_id(status):
            raise ValidationException("Invalid blog status.")

        sanitized_html = sanitize_html(payload.content.contentHtml)
        reading_time = calculate_reading_time(sanitized_html, payload.content.contentBlocks)
        metadata = payload.metadata.model_dump()
        content = payload.content.model_dump()
        self._validate_publish_requirements(status, metadata, sanitized_html)

        timestamp = utc_now_iso()
        blog_id = generate_id()
        metadata_item = {
            "blogId": blog_id,
            "slug": slug,
            "title": metadata.get("title"),
            "shortDescription": metadata.get("shortDescription"),
            "coverImageUrl": metadata.get("coverImageUrl"),
            "authorId": metadata.get("authorId") or current_user["userId"],
            "categoryId": metadata.get("categoryId"),
            "tagIds": metadata.get("tagIds", []),
            "blogStatus": status,
            "isFeatured": metadata.get("isFeatured", False),
            "isTrending": metadata.get("isTrending", False),
            "readingTimeMinutes": reading_time,
            "publishedAt": timestamp if status == PUBLISHED_STATUS_ID else None,
            "createdAt": timestamp,
            "modifiedAt": timestamp,
            "seoTitle": metadata.get("seoTitle"),
            "seoDescription": metadata.get("seoDescription"),
            "seoKeywords": metadata.get("seoKeywords", []),
            "createdBy": current_user["userId"],
            "modifiedBy": current_user["userId"],
            "isDeleted": False,
        }
        content_item = {
            "blogId": blog_id,
            "contentHtml": sanitized_html,
            "contentBlocks": content.get("contentBlocks", []),
            "createdAt": timestamp,
            "modifiedAt": timestamp,
            "isDeleted": False,
        }
        analytics_item = {
            "blogId": blog_id,
            "totalViews": 0,
            "totalLikes": 0,
            "totalShares": 0,
            "viewsByDate": {},
            "lastViewedAt": None,
            "updatedAt": timestamp,
            "isDeleted": False,
        }
        self.blog_metadata_repository.save(metadata_item)
        self.blog_content_repository.save(content_item)
        self.blog_analytics_repository.save(analytics_item)
        return self.get_blog(blog_id)

    def get_blog(self, blog_id: str) -> AdminBlogDetailResponse:
        metadata = self.blog_metadata_repository.get_by_id(blog_id)
        if not metadata:
            raise NotFoundException("Blog not found.")
        content = self.blog_content_repository.get_by_blog_id(blog_id)
        analytics = self.blog_analytics_repository.get_by_blog_id(blog_id)
        return AdminBlogDetailResponse(
            blogId=blog_id,
            metadata=metadata,
            content=content or {"contentHtml": "", "contentBlocks": []},
            analytics=self._analytics_summary(analytics),
        )

    def update_blog(self, blog_id: str, payload: UpdateBlogRequest, current_user: dict) -> AdminBlogDetailResponse:
        existing = self.blog_metadata_repository.get_by_id(blog_id)
        if not existing:
            raise NotFoundException("Blog not found.")

        self._validate_payload(payload.metadata.categoryId, payload.metadata.tagIds)
        slug = slugify(payload.metadata.slug or payload.metadata.title or existing["slug"])
        if self.blog_metadata_repository.get_by_slug(slug, exclude_blog_id=blog_id):
            raise ConflictException("Blog slug already exists.")

        sanitized_html = sanitize_html(payload.content.contentHtml)
        reading_time = calculate_reading_time(sanitized_html, payload.content.contentBlocks)

        existing.update(
            {
                "slug": slug,
                "title": payload.metadata.title,
                "shortDescription": payload.metadata.shortDescription,
                "coverImageUrl": payload.metadata.coverImageUrl,
                "authorId": payload.metadata.authorId or existing["authorId"],
                "categoryId": payload.metadata.categoryId,
                "tagIds": payload.metadata.tagIds,
                "isFeatured": payload.metadata.isFeatured,
                "isTrending": payload.metadata.isTrending,
                "readingTimeMinutes": reading_time,
                "seoTitle": payload.metadata.seoTitle,
                "seoDescription": payload.metadata.seoDescription,
                "seoKeywords": payload.metadata.seoKeywords,
                "modifiedAt": utc_now_iso(),
                "modifiedBy": current_user["userId"],
            }
        )
        if existing["blogStatus"] == PUBLISHED_STATUS_ID:
            self._validate_publish_requirements(existing["blogStatus"], payload.metadata.model_dump(), sanitized_html)
        self.blog_metadata_repository.save(existing)

        content_item = self.blog_content_repository.get_by_blog_id(blog_id) or {
            "blogId": blog_id,
            "createdAt": utc_now_iso(),
            "isDeleted": False,
        }
        content_item.update(
            {
                "contentHtml": sanitized_html,
                "contentBlocks": payload.content.contentBlocks,
                "modifiedAt": utc_now_iso(),
            }
        )
        self.blog_content_repository.save(content_item)
        return self.get_blog(blog_id)

    def update_blog_status(self, blog_id: str, status: str, current_user: dict) -> AdminBlogDetailResponse:
        blog = self.blog_metadata_repository.get_by_id(blog_id)
        if not blog:
            raise NotFoundException("Blog not found.")
        if not self.blog_status_repository.get_by_id(status):
            raise ValidationException("Invalid blog status.")

        content = self.blog_content_repository.get_by_blog_id(blog_id) or {"contentHtml": "", "contentBlocks": []}
        self._validate_publish_requirements(status, blog, content.get("contentHtml"))

        blog["blogStatus"] = status
        blog["modifiedAt"] = utc_now_iso()
        blog["modifiedBy"] = current_user["userId"]
        if status == PUBLISHED_STATUS_ID and not blog["publishedAt"]:
            blog["publishedAt"] = utc_now_iso()
        self.blog_metadata_repository.save(blog)
        return self.get_blog(blog_id)

    def delete_blog(self, blog_id: str) -> None:
        blog = self.blog_metadata_repository.get_by_id(blog_id)
        if not blog:
            raise NotFoundException("Blog not found.")
        self.blog_metadata_repository.soft_delete(blog_id)
        self.blog_content_repository.soft_delete(blog_id)

    def generate_preview(self, payload: CreateBlogRequest | UpdateBlogRequest) -> BlogPreviewResponse:
        sanitized_html = sanitize_html(payload.content.contentHtml)
        return BlogPreviewResponse(
            metadata=payload.metadata.model_dump(),
            content={"contentHtml": sanitized_html, "contentBlocks": payload.content.contentBlocks},
            derived={"readingTimeMinutes": calculate_reading_time(sanitized_html, payload.content.contentBlocks)},
        )

    def _validate_payload(self, category_id: str | None, tag_ids: list[str]) -> None:
        if category_id and not self.category_repository.get_by_id(category_id):
            raise ValidationException("Category does not exist.")
        missing_tags = [tag_id for tag_id in tag_ids if not self.tag_repository.get_by_id(tag_id)]
        if missing_tags:
            raise ValidationException(f"Invalid tag ids: {', '.join(missing_tags)}")

    def _validate_publish_requirements(self, status: str, metadata: dict, content_html: str | None) -> None:
        if status != PUBLISHED_STATUS_ID:
            return
        required_fields = {
            "title": metadata.get("title"),
            "slug": metadata.get("slug") or slugify(metadata.get("title") or ""),
            "shortDescription": metadata.get("shortDescription"),
            "coverImageUrl": metadata.get("coverImageUrl"),
            "categoryId": metadata.get("categoryId"),
            "seoTitle": metadata.get("seoTitle"),
            "seoDescription": metadata.get("seoDescription"),
        }
        missing_fields = [field_name for field_name, value in required_fields.items() if not value]
        if not metadata.get("tagIds"):
            missing_fields.append("tagIds")
        if not content_html:
            missing_fields.append("content")
        if missing_fields:
            raise ValidationException(f"Publishing requires these fields: {', '.join(missing_fields)}")

    def _to_list_item(self, item: dict) -> AdminBlogListItem:
        category = self.category_repository.get_by_id(item["categoryId"]) if item.get("categoryId") else None
        return AdminBlogListItem(
            blogId=item["blogId"],
            title=item["title"] or "",
            slug=item["slug"],
            status=item["blogStatus"],
            categoryId=item["categoryId"],
            categoryLabel=category["categoryLabel"] if category else None,
            publishedAt=item["publishedAt"],
            modifiedAt=item["modifiedAt"],
        )

    def _analytics_summary(self, item: dict | None) -> BlogAnalyticsSummary:
        if not item:
            return BlogAnalyticsSummary(totalViews=0, totalLikes=0, totalShares=0)
        return BlogAnalyticsSummary(
            totalViews=item["totalViews"],
            totalLikes=item["totalLikes"],
            totalShares=item["totalShares"],
        )
