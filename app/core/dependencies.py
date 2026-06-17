from typing import Annotated

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.core.container import get_container
from app.services.admin.analytics_service import AnalyticsService
from app.services.admin.asset_service import AssetService
from app.services.admin.auth_service import AuthService
from app.services.admin.blog_preview_service import BlogPreviewService
from app.services.admin.blog_service import BlogService
from app.services.admin.category_service import CategoryService
from app.services.admin.dashboard_service import DashboardService
from app.services.admin.master_service import MasterService
from app.services.admin.tag_service import TagService
from app.services.admin.user_service import UserService

bearer_scheme = HTTPBearer(auto_error=False)


def get_auth_service() -> AuthService:
    return get_container().auth_service


def get_category_service() -> CategoryService:
    return get_container().category_service


def get_user_service() -> UserService:
    return get_container().user_service


def get_tag_service() -> TagService:
    return get_container().tag_service


def get_asset_service() -> AssetService:
    return get_container().asset_service


def get_blog_service() -> BlogService:
    return get_container().blog_service


def get_blog_preview_service() -> BlogPreviewService:
    return get_container().blog_preview_service


def get_dashboard_service() -> DashboardService:
    return get_container().dashboard_service


def get_analytics_service() -> AnalyticsService:
    return get_container().analytics_service


def get_master_service() -> MasterService:
    return get_container().master_service


def get_current_admin_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer_scheme)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict:
    if credentials is None:
        return auth_service.raise_unauthorized()
    return auth_service.get_user_from_token(credentials.credentials)
