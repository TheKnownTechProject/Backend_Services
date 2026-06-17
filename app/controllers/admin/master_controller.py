from app.schemas.common.api_response import ApiResponse


def blog_statuses(items) -> ApiResponse:
    return ApiResponse(message="Blog statuses fetched successfully.", data={"items": items})
