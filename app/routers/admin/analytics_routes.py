from typing import Annotated

from fastapi import APIRouter, Depends

from app.controllers.admin import analytics_controller
from app.core.dependencies import get_analytics_service, get_current_admin_user
from app.services.admin.analytics_service import AnalyticsService

router = APIRouter()


@router.get("/overview")
def overview(
    _: Annotated[dict, Depends(get_current_admin_user)],
    analytics_service: Annotated[AnalyticsService, Depends(get_analytics_service)],
):
    return analytics_controller.analytics_overview(analytics_service.get_overview())


@router.get("/blogs")
def list_blog_metrics(
    _: Annotated[dict, Depends(get_current_admin_user)],
    analytics_service: Annotated[AnalyticsService, Depends(get_analytics_service)],
):
    return analytics_controller.analytics_list(analytics_service.list_blog_metrics())


@router.get("/blogs/{blog_id}")
def blog_metric_detail(
    blog_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    analytics_service: Annotated[AnalyticsService, Depends(get_analytics_service)],
):
    return analytics_controller.analytics_detail(analytics_service.get_blog_analytics(blog_id))
