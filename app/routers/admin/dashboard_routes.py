from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.controllers.admin import dashboard_controller
from app.core.dependencies import get_current_admin_user, get_dashboard_service
from app.services.admin.dashboard_service import DashboardService

router = APIRouter()


@router.get("/summary")
def summary(
    _: Annotated[dict, Depends(get_current_admin_user)],
    dashboard_service: Annotated[DashboardService, Depends(get_dashboard_service)],
):
    return dashboard_controller.dashboard_summary(dashboard_service.get_summary())


@router.get("/top-blogs")
def top_blogs(
    _: Annotated[dict, Depends(get_current_admin_user)],
    dashboard_service: Annotated[DashboardService, Depends(get_dashboard_service)],
    limit: int = Query(default=5, ge=1, le=20),
):
    return dashboard_controller.top_blogs(dashboard_service.get_top_blogs(limit))
