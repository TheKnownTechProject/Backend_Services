from app.schemas.common.api_response import ApiResponse


def list_users(items) -> ApiResponse:
    return ApiResponse(message="Users fetched successfully.", data={"items": [item.model_dump() for item in items]})


def user_detail(item) -> ApiResponse:
    return ApiResponse(message="User fetched successfully.", data=item.model_dump())


def user_created(item) -> ApiResponse:
    return ApiResponse(message="User created successfully.", data=item.model_dump())


def user_updated(item) -> ApiResponse:
    return ApiResponse(message="User updated successfully.", data=item.model_dump())


def user_deleted() -> ApiResponse:
    return ApiResponse(message="User deleted successfully.")
