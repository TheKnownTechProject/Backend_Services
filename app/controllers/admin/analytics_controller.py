from app.schemas.common.api_response import ApiResponse


def analytics_overview(item) -> ApiResponse:
    return ApiResponse(message="Analytics overview fetched successfully.", data=item.model_dump())


def analytics_list(items) -> ApiResponse:
    return ApiResponse(message="Blog analytics fetched successfully.", data={"items": [item.model_dump() for item in items]})


def analytics_detail(item) -> ApiResponse:
    return ApiResponse(message="Blog analytics detail fetched successfully.", data=item.model_dump())
