from typing import Annotated

from fastapi import APIRouter, Depends

from app.controllers.admin import category_controller
from app.core.dependencies import get_category_service, get_current_admin_user
from app.schemas.admin.category_schema import CreateCategoryRequest, UpdateCategoryRequest
from app.services.admin.category_service import CategoryService

router = APIRouter()


@router.get("")
def list_categories(
    _: Annotated[dict, Depends(get_current_admin_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return category_controller.list_categories(category_service.list_categories())


@router.post("")
def create_category(
    payload: CreateCategoryRequest,
    _: Annotated[dict, Depends(get_current_admin_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return category_controller.category_created(category_service.create_category(payload))


@router.get("/{category_id}")
def get_category(
    category_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return category_controller.category_detail(category_service.get_category(category_id))


@router.put("/{category_id}")
def update_category(
    category_id: str,
    payload: UpdateCategoryRequest,
    _: Annotated[dict, Depends(get_current_admin_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    return category_controller.category_updated(category_service.update_category(category_id, payload))


@router.delete("/{category_id}")
def delete_category(
    category_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    category_service: Annotated[CategoryService, Depends(get_category_service)],
):
    category_service.delete_category(category_id)
    return category_controller.category_deleted()
