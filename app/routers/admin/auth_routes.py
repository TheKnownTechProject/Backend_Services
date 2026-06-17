from typing import Annotated

from fastapi import APIRouter, Depends

from app.controllers.admin import auth_controller
from app.core.dependencies import get_auth_service, get_current_admin_user
from app.schemas.admin.auth_schema import LoginRequest
from app.services.admin.auth_service import AuthService

router = APIRouter()


@router.post("/login")
def login(
    payload: LoginRequest,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return auth_controller.login(auth_service.login(payload.email, payload.password))


@router.get("/login-user-details")
def login_user_details(
    current_user: Annotated[dict, Depends(get_current_admin_user)],
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
):
    return auth_controller.login_user_details(auth_service.get_login_user_details(current_user))
