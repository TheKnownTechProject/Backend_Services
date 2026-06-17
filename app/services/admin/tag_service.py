from app.core.exceptions import ConflictException, NotFoundException, ValidationException
from app.repositories.db.blog_metadata_repository import BlogMetadataRepository
from app.repositories.db.category_repository import CategoryRepository
from app.repositories.db.tag_repository import TagRepository
from app.schemas.admin.tag_schema import CreateTagRequest, TagResponse, UpdateTagRequest
from app.utils.datetime import utc_now_iso
from app.utils.id_generator import generate_id
from app.utils.slug import slugify


class TagService:
    def __init__(
        self,
        tag_repository: TagRepository,
        category_repository: CategoryRepository,
        blog_metadata_repository: BlogMetadataRepository,
    ):
        self.tag_repository = tag_repository
        self.category_repository = category_repository
        self.blog_metadata_repository = blog_metadata_repository

    def list_tags(self) -> list[TagResponse]:
        return [self._to_response(item) for item in self.tag_repository.list_all()]

    def get_tag(self, tag_id: str) -> TagResponse:
        tag = self.tag_repository.get_by_id(tag_id)
        if not tag:
            raise NotFoundException("Tag not found.")
        return self._to_response(tag)

    def create_tag(self, payload: CreateTagRequest) -> TagResponse:
        slug = slugify(payload.slug or payload.tagLabel)
        if self.tag_repository.get_by_slug(slug):
            raise ConflictException("Tag slug already exists.")
        self._validate_category_ids(payload.categoryIds)

        timestamp = utc_now_iso()
        item = {
            "tagId": generate_id(),
            "tagLabel": payload.tagLabel.strip(),
            "slug": slug,
            "categoryIds": payload.categoryIds,
            "blogCount": 0,
            "isActive": payload.isActive,
            "createdAt": timestamp,
            "modifiedAt": timestamp,
            "isDeleted": False,
        }
        return self._to_response(self.tag_repository.save(item))

    def update_tag(self, tag_id: str, payload: UpdateTagRequest) -> TagResponse:
        existing = self.tag_repository.get_by_id(tag_id)
        if not existing:
            raise NotFoundException("Tag not found.")

        slug = slugify(payload.slug or payload.tagLabel)
        if self.tag_repository.get_by_slug(slug, exclude_tag_id=tag_id):
            raise ConflictException("Tag slug already exists.")
        self._validate_category_ids(payload.categoryIds)

        existing.update(
            {
                "tagLabel": payload.tagLabel.strip(),
                "slug": slug,
                "categoryIds": payload.categoryIds,
                "isActive": payload.isActive,
                "modifiedAt": utc_now_iso(),
            }
        )
        return self._to_response(self.tag_repository.save(existing))

    def delete_tag(self, tag_id: str) -> None:
        tag = self.tag_repository.get_by_id(tag_id)
        if not tag:
            raise NotFoundException("Tag not found.")
        if self.blog_metadata_repository.count_by_tag_id(tag_id) > 0:
            raise ConflictException("Tag cannot be deleted because it is mapped to one or more blogs.")
        self.tag_repository.soft_delete(tag_id)

    def _validate_category_ids(self, category_ids: list[str]) -> None:
        missing_ids = [category_id for category_id in category_ids if not self.category_repository.get_by_id(category_id)]
        if missing_ids:
            raise ValidationException(f"Invalid category ids: {', '.join(missing_ids)}")

    def _to_response(self, item: dict) -> TagResponse:
        return TagResponse(
            tagId=item["tagId"],
            tagLabel=item["tagLabel"],
            slug=item["slug"],
            categoryIds=item["categoryIds"],
            blogCount=self.blog_metadata_repository.count_by_tag_id(item["tagId"]),
            isActive=item["isActive"],
            createdAt=item["createdAt"],
            modifiedAt=item["modifiedAt"],
        )
