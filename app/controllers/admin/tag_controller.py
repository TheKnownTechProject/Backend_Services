from app.schemas.common.api_response import ApiResponse


def list_tags(items) -> ApiResponse:
    return ApiResponse(message="Tags fetched successfully.", data={"items": [item.model_dump() for item in items]})


def tag_detail(item) -> ApiResponse:
    return ApiResponse(message="Tag fetched successfully.", data=item.model_dump())


def tag_created(item) -> ApiResponse:
    return ApiResponse(message="Tag created successfully.", data=item.model_dump())


def tag_updated(item) -> ApiResponse:
    return ApiResponse(message="Tag updated successfully.", data=item.model_dump())


def tag_deleted() -> ApiResponse:
    return ApiResponse(message="Tag deleted successfully.")
