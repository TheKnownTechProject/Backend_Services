from app.schemas.common.api_response import ApiResponse


def login(login_response) -> ApiResponse:
    return ApiResponse(message="Login successful.", data=login_response.model_dump())


def login_user_details(user_response) -> ApiResponse:
    return ApiResponse(message="Logged in user fetched successfully.", data=user_response.model_dump())
