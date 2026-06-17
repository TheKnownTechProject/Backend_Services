from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


class AppException(Exception):
    status_code = 400
    code = "app_error"

    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class ValidationException(AppException):
    status_code = 422
    code = "validation_error"


class NotFoundException(AppException):
    status_code = 404
    code = "not_found"


class ConflictException(AppException):
    status_code = 409
    code = "conflict"


class UnauthorizedException(AppException):
    status_code = 401
    code = "unauthorized"


class ForbiddenException(AppException):
    status_code = 403
    code = "forbidden"


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(AppException)
    async def handle_app_exception(_: Request, exc: AppException) -> JSONResponse:
        return JSONResponse(
            status_code=exc.status_code,
            content={"success": False, "message": exc.message, "errorCode": exc.code},
        )
