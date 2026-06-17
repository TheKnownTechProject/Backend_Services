from typing import Annotated

from fastapi import APIRouter, Depends

from app.controllers.admin import user_controller
from app.core.dependencies import get_current_admin_user, get_user_service
from app.schemas.admin.user_schema import CreateUserRequest, UpdateUserRequest
from app.services.admin.user_service import UserService

router = APIRouter()


@router.get("")
def list_users(
    _: Annotated[dict, Depends(get_current_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_controller.list_users(user_service.list_users())


@router.post("")
def create_user(
    payload: CreateUserRequest,
    _: Annotated[dict, Depends(get_current_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_controller.user_created(user_service.create_user(payload))


@router.get("/{user_id}")
def get_user(
    user_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_controller.user_detail(user_service.get_user(user_id))


@router.put("/{user_id}")
def update_user(
    user_id: str,
    payload: UpdateUserRequest,
    _: Annotated[dict, Depends(get_current_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    return user_controller.user_updated(user_service.update_user(user_id, payload))


@router.delete("/{user_id}")
def delete_user(
    user_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    user_service: Annotated[UserService, Depends(get_user_service)],
):
    user_service.delete_user(user_id)
    return user_controller.user_deleted()
