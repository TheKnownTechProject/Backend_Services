from typing import Annotated

from fastapi import APIRouter, Depends, File, Form, Query, UploadFile

from app.controllers.admin import asset_controller
from app.core.config import get_settings
from app.core.dependencies import get_asset_service, get_current_admin_user
from app.services.admin.asset_service import AssetService

router = APIRouter()


@router.get("")
def list_assets(
    _: Annotated[dict, Depends(get_current_admin_user)],
    asset_service: Annotated[AssetService, Depends(get_asset_service)],
    cursor: str | None = Query(default=None),
    limit: int = Query(default=get_settings().default_page_size, ge=1, le=get_settings().max_page_size),
    assetType: str | None = Query(default=None),
):
    items, next_cursor = asset_service.list_assets(cursor, limit, assetType)
    return asset_controller.list_assets(items, next_cursor, limit)


@router.post("")
async def upload_asset(
    current_user: Annotated[dict, Depends(get_current_admin_user)],
    asset_service: Annotated[AssetService, Depends(get_asset_service)],
    file: UploadFile = File(...),
    altText: str | None = Form(default=None),
    assetType: str = Form(...),
):
    content = await file.read()
    item = asset_service.upload_asset(
        file_name=file.filename or "",
        mime_type=file.content_type or "application/octet-stream",
        content=content,
        alt_text=altText,
        asset_type=assetType,
        uploaded_by=current_user["userId"],
    )
    return asset_controller.asset_uploaded(item)


@router.get("/{asset_id}")
def get_asset(
    asset_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    asset_service: Annotated[AssetService, Depends(get_asset_service)],
):
    return asset_controller.asset_detail(asset_service.get_asset(asset_id))


@router.delete("/{asset_id}")
def delete_asset(
    asset_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    asset_service: Annotated[AssetService, Depends(get_asset_service)],
):
    asset_service.delete_asset(asset_id)
    return asset_controller.asset_deleted()
