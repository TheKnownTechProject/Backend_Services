from app.schemas.common.api_response import ApiResponse


def list_blogs(items, next_cursor: str | None, limit: int) -> ApiResponse:
    return ApiResponse(
        message="Blogs fetched successfully.",
        data={"items": [item.model_dump() for item in items]},
        meta={"nextCursor": next_cursor, "limit": limit},
    )


def blog_detail(item) -> ApiResponse:
    return ApiResponse(message="Blog fetched successfully.", data=item.model_dump())


def blog_created(item) -> ApiResponse:
    return ApiResponse(message="Blog created successfully.", data=item.model_dump())


def blog_updated(item) -> ApiResponse:
    return ApiResponse(message="Blog updated successfully.", data=item.model_dump())


def blog_deleted() -> ApiResponse:
    return ApiResponse(message="Blog deleted successfully.")


def blog_preview(item) -> ApiResponse:
    return ApiResponse(message="Blog preview generated successfully.", data=item.model_dump())
