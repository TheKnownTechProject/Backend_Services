from app.core.exceptions import ConflictException, NotFoundException
from app.repositories.db.blog_metadata_repository import BlogMetadataRepository
from app.repositories.db.category_repository import CategoryRepository
from app.repositories.db.tag_repository import TagRepository
from app.schemas.admin.category_schema import CategoryResponse, CreateCategoryRequest, UpdateCategoryRequest
from app.utils.datetime import utc_now_iso
from app.utils.id_generator import generate_id
from app.utils.slug import slugify


class CategoryService:
    def __init__(
        self,
        category_repository: CategoryRepository,
        tag_repository: TagRepository,
        blog_metadata_repository: BlogMetadataRepository,
    ):
        self.category_repository = category_repository
        self.tag_repository = tag_repository
        self.blog_metadata_repository = blog_metadata_repository

    def list_categories(self) -> list[CategoryResponse]:
        return [self._to_response(item) for item in self.category_repository.list_all()]

    def get_category(self, category_id: str) -> CategoryResponse:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise NotFoundException("Category not found.")
        return self._to_response(category)

    def create_category(self, payload: CreateCategoryRequest) -> CategoryResponse:
        slug = slugify(payload.slug or payload.categoryLabel)
        if self.category_repository.get_by_slug(slug):
            raise ConflictException("Category slug already exists.")

        timestamp = utc_now_iso()
        item = {
            "categoryId": generate_id(),
            "categoryLabel": payload.categoryLabel.strip(),
            "slug": slug,
            "description": payload.description,
            "isActive": payload.isActive,
            "blogCount": 0,
            "createdAt": timestamp,
            "modifiedAt": timestamp,
            "isDeleted": False,
        }
        return self._to_response(self.category_repository.save(item))

    def update_category(self, category_id: str, payload: UpdateCategoryRequest) -> CategoryResponse:
        existing = self.category_repository.get_by_id(category_id)
        if not existing:
            raise NotFoundException("Category not found.")

        slug = slugify(payload.slug or payload.categoryLabel)
        if self.category_repository.get_by_slug(slug, exclude_category_id=category_id):
            raise ConflictException("Category slug already exists.")

        existing.update(
            {
                "categoryLabel": payload.categoryLabel.strip(),
                "slug": slug,
                "description": payload.description,
                "isActive": payload.isActive,
                "modifiedAt": utc_now_iso(),
            }
        )
        return self._to_response(self.category_repository.save(existing))

    def delete_category(self, category_id: str) -> None:
        category = self.category_repository.get_by_id(category_id)
        if not category:
            raise NotFoundException("Category not found.")

        if self.blog_metadata_repository.count_by_category_id(category_id) > 0:
            raise ConflictException("Category cannot be deleted because it is mapped to one or more blogs.")

        if any(category_id in tag["categoryIds"] for tag in self.tag_repository.list_all()):
            raise ConflictException("Category cannot be deleted because it is mapped to one or more tags.")

        self.category_repository.soft_delete(category_id)

    def _to_response(self, item: dict) -> CategoryResponse:
        return CategoryResponse(
            categoryId=item["categoryId"],
            categoryLabel=item["categoryLabel"],
            slug=item["slug"],
            description=item["description"],
            isActive=item["isActive"],
            blogCount=self.blog_metadata_repository.count_by_category_id(item["categoryId"]),
            createdAt=item["createdAt"],
            modifiedAt=item["modifiedAt"],
        )
