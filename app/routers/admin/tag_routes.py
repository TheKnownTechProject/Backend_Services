from typing import Annotated

from fastapi import APIRouter, Depends

from app.controllers.admin import tag_controller
from app.core.dependencies import get_current_admin_user, get_tag_service
from app.schemas.admin.tag_schema import CreateTagRequest, UpdateTagRequest
from app.services.admin.tag_service import TagService

router = APIRouter()


@router.get("")
def list_tags(
    _: Annotated[dict, Depends(get_current_admin_user)],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
):
    return tag_controller.list_tags(tag_service.list_tags())


@router.post("")
def create_tag(
    payload: CreateTagRequest,
    _: Annotated[dict, Depends(get_current_admin_user)],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
):
    return tag_controller.tag_created(tag_service.create_tag(payload))


@router.get("/{tag_id}")
def get_tag(
    tag_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
):
    return tag_controller.tag_detail(tag_service.get_tag(tag_id))


@router.put("/{tag_id}")
def update_tag(
    tag_id: str,
    payload: UpdateTagRequest,
    _: Annotated[dict, Depends(get_current_admin_user)],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
):
    return tag_controller.tag_updated(tag_service.update_tag(tag_id, payload))


@router.delete("/{tag_id}")
def delete_tag(
    tag_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    tag_service: Annotated[TagService, Depends(get_tag_service)],
):
    tag_service.delete_tag(tag_id)
    return tag_controller.tag_deleted()
