from app.schemas.common.api_response import ApiResponse


def dashboard_summary(item) -> ApiResponse:
    return ApiResponse(message="Dashboard summary fetched successfully.", data=item.model_dump())


def top_blogs(items) -> ApiResponse:
    return ApiResponse(message="Top blogs fetched successfully.", data={"items": [item.model_dump() for item in items]})
