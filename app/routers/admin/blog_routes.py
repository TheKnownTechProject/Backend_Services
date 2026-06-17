from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.controllers.admin import blog_controller
from app.core.config import get_settings
from app.core.dependencies import get_blog_preview_service, get_blog_service, get_current_admin_user
from app.schemas.admin.blog_schema import BlogPreviewRequest, CreateBlogRequest, UpdateBlogRequest, UpdateBlogStatusRequest
from app.services.admin.blog_preview_service import BlogPreviewService
from app.services.admin.blog_service import BlogService

router = APIRouter()


@router.get("")
def list_blogs(
    _: Annotated[dict, Depends(get_current_admin_user)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
    cursor: str | None = Query(default=None),
    limit: int = Query(default=get_settings().default_page_size, ge=1, le=get_settings().max_page_size),
    status: str | None = Query(default=None),
    search: str | None = Query(default=None),
    categoryId: str | None = Query(default=None),
):
    items, next_cursor = blog_service.list_blogs(cursor, limit, status, search, categoryId)
    return blog_controller.list_blogs(items, next_cursor, limit)


@router.post("")
def create_blog(
    payload: CreateBlogRequest,
    current_user: Annotated[dict, Depends(get_current_admin_user)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
):
    return blog_controller.blog_created(blog_service.create_blog(payload, current_user))


@router.post("/preview")
def preview_blog(
    payload: BlogPreviewRequest,
    _: Annotated[dict, Depends(get_current_admin_user)],
    preview_service: Annotated[BlogPreviewService, Depends(get_blog_preview_service)],
):
    return blog_controller.blog_preview(preview_service.generate_preview(payload))


@router.get("/{blog_id}")
def get_blog(
    blog_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
):
    return blog_controller.blog_detail(blog_service.get_blog(blog_id))


@router.put("/{blog_id}")
def update_blog(
    blog_id: str,
    payload: UpdateBlogRequest,
    current_user: Annotated[dict, Depends(get_current_admin_user)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
):
    return blog_controller.blog_updated(blog_service.update_blog(blog_id, payload, current_user))


@router.patch("/{blog_id}/status")
def update_blog_status(
    blog_id: str,
    payload: UpdateBlogStatusRequest,
    current_user: Annotated[dict, Depends(get_current_admin_user)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
):
    return blog_controller.blog_updated(blog_service.update_blog_status(blog_id, payload.status, current_user))


@router.delete("/{blog_id}")
def delete_blog(
    blog_id: str,
    _: Annotated[dict, Depends(get_current_admin_user)],
    blog_service: Annotated[BlogService, Depends(get_blog_service)],
):
    blog_service.delete_blog(blog_id)
    return blog_controller.blog_deleted()
