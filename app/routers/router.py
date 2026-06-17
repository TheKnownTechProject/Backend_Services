from fastapi import APIRouter

from app.routers.admin.router import router as admin_router

router = APIRouter()


@router.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


router.include_router(admin_router, prefix="/admin", tags=["Admin"])
