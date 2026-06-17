from app.core.exceptions import ValidationException
from app.repositories.db.category_repository import CategoryRepository
from app.repositories.db.tag_repository import TagRepository
from app.schemas.admin.blog_schema import BlogPreviewRequest, BlogPreviewResponse
from app.utils.html_sanitizer import sanitize_html
from app.utils.reading_time import calculate_reading_time


class BlogPreviewService:
    def __init__(self, category_repository: CategoryRepository, tag_repository: TagRepository):
        self.category_repository = category_repository
        self.tag_repository = tag_repository

    def generate_preview(self, payload: BlogPreviewRequest) -> BlogPreviewResponse:
        category_id = payload.metadata.categoryId
        if category_id and not self.category_repository.get_by_id(category_id):
            raise ValidationException("Category does not exist.")

        missing_tags = [tag_id for tag_id in payload.metadata.tagIds if not self.tag_repository.get_by_id(tag_id)]
        if missing_tags:
            raise ValidationException(f"Invalid tag ids: {', '.join(missing_tags)}")

        sanitized_content = sanitize_html(payload.content.contentHtml)
        reading_time = calculate_reading_time(sanitized_content, payload.content.contentBlocks)
        return BlogPreviewResponse(
            metadata=payload.metadata.model_dump(),
            content={
                "contentHtml": sanitized_content,
                "contentBlocks": payload.content.contentBlocks,
            },
            derived={"readingTimeMinutes": reading_time},
        )
