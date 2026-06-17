from app.schemas.common.api_response import ApiResponse


def list_categories(items) -> ApiResponse:
    return ApiResponse(message="Categories fetched successfully.", data={"items": [item.model_dump() for item in items]})


def category_detail(item) -> ApiResponse:
    return ApiResponse(message="Category fetched successfully.", data=item.model_dump())


def category_created(item) -> ApiResponse:
    return ApiResponse(message="Category created successfully.", data=item.model_dump())


def category_updated(item) -> ApiResponse:
    return ApiResponse(message="Category updated successfully.", data=item.model_dump())


def category_deleted() -> ApiResponse:
    return ApiResponse(message="Category deleted successfully.")
