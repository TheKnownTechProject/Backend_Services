from typing import Annotated

from fastapi import APIRouter, Depends

from app.controllers.admin import master_controller
from app.core.dependencies import get_current_admin_user, get_master_service
from app.services.admin.master_service import MasterService

router = APIRouter()


@router.get("/blog-statuses")
def blog_statuses(
    _: Annotated[dict, Depends(get_current_admin_user)],
    master_service: Annotated[MasterService, Depends(get_master_service)],
):
    return master_controller.blog_statuses(master_service.list_blog_statuses())
