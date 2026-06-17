from app.schemas.common.api_response import ApiResponse


def list_assets(items, next_cursor: str | None, limit: int) -> ApiResponse:
    return ApiResponse(
        message="Assets fetched successfully.",
        data={"items": [item.model_dump() for item in items]},
        meta={"nextCursor": next_cursor, "limit": limit},
    )


def asset_detail(item) -> ApiResponse:
    return ApiResponse(message="Asset fetched successfully.", data=item.model_dump())


def asset_uploaded(item) -> ApiResponse:
    return ApiResponse(message="Asset uploaded successfully.", data=item.model_dump())


def asset_deleted() -> ApiResponse:
    return ApiResponse(message="Asset deleted successfully.")
