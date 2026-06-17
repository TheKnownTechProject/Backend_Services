from dataclasses import dataclass
from functools import lru_cache

from app.core.config import get_settings
from app.core.constants import MASTER_STATUSES
from app.core.security import hash_password
from app.repositories.db.base_repository import InMemoryDataStore
from app.repositories.db.blog_analytics_repository import BlogAnalyticsRepository
from app.repositories.db.blog_asset_repository import BlogAssetRepository
from app.repositories.db.blog_content_repository import BlogContentRepository
from app.repositories.db.blog_metadata_repository import BlogMetadataRepository
from app.repositories.db.blog_status_repository import BlogStatusRepository
from app.repositories.db.category_repository import CategoryRepository
from app.repositories.db.tag_repository import TagRepository
from app.repositories.db.user_repository import UserRepository
from app.repositories.s3.asset_storage_repository import LocalAssetStorageRepository
from app.services.admin.analytics_service import AnalyticsService
from app.services.admin.asset_service import AssetService
from app.services.admin.auth_service import AuthService
from app.services.admin.blog_preview_service import BlogPreviewService
from app.services.admin.blog_service import BlogService
from app.services.admin.category_service import CategoryService
from app.services.admin.dashboard_service import DashboardService
from app.services.admin.master_service import MasterService
from app.services.admin.tag_service import TagService


@dataclass
class Container:
    auth_service: AuthService
    category_service: CategoryService
    tag_service: TagService
    asset_service: AssetService
    blog_service: BlogService
    blog_preview_service: BlogPreviewService
    dashboard_service: DashboardService
    analytics_service: AnalyticsService
    master_service: MasterService


def seed_store(store: InMemoryDataStore) -> None:
    settings = get_settings()

    for status in MASTER_STATUSES:
        store.blog_statuses[status["status_id"]] = {
            "statusId": status["status_id"],
            "statusLabel": status["status_label"],
            "description": status["description"],
            "isActive": status["is_active"],
        }

    if not store.users:
        store.users["seed-admin"] = {
            "userId": "seed-admin",
            "name": settings.admin_seed_name,
            "email": settings.admin_seed_email.lower(),
            "passwordHash": hash_password(settings.admin_seed_password),
            "profileImageUrl": None,
            "bio": None,
            "isActive": True,
            "isDeleted": False,
        }


@lru_cache
def get_container() -> Container:
    store = InMemoryDataStore()
    seed_store(store)

    user_repository = UserRepository(store)
    category_repository = CategoryRepository(store)
    tag_repository = TagRepository(store)
    blog_metadata_repository = BlogMetadataRepository(store)
    blog_content_repository = BlogContentRepository(store)
    blog_analytics_repository = BlogAnalyticsRepository(store)
    blog_asset_repository = BlogAssetRepository(store)
    blog_status_repository = BlogStatusRepository(store)
    asset_storage_repository = LocalAssetStorageRepository()

    auth_service = AuthService(user_repository)
    category_service = CategoryService(category_repository, tag_repository, blog_metadata_repository)
    tag_service = TagService(tag_repository, category_repository, blog_metadata_repository)
    asset_service = AssetService(blog_asset_repository, asset_storage_repository)
    blog_service = BlogService(
        blog_metadata_repository,
        blog_content_repository,
        blog_analytics_repository,
        category_repository,
        tag_repository,
        blog_status_repository,
    )
    blog_preview_service = BlogPreviewService(category_repository, tag_repository)
    dashboard_service = DashboardService(blog_analytics_repository, blog_metadata_repository)
    analytics_service = AnalyticsService(blog_analytics_repository, blog_metadata_repository)
    master_service = MasterService(blog_status_repository)

    return Container(
        auth_service=auth_service,
        category_service=category_service,
        tag_service=tag_service,
        asset_service=asset_service,
        blog_service=blog_service,
        blog_preview_service=blog_preview_service,
        dashboard_service=dashboard_service,
        analytics_service=analytics_service,
        master_service=master_service,
    )
