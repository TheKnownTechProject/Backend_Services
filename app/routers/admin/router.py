from fastapi import APIRouter

from app.routers.admin.analytics_routes import router as analytics_router
from app.routers.admin.asset_routes import router as asset_router
from app.routers.admin.auth_routes import router as auth_router
from app.routers.admin.blog_routes import router as blog_router
from app.routers.admin.category_routes import router as category_router
from app.routers.admin.dashboard_routes import router as dashboard_router
from app.routers.admin.master_routes import router as master_router
from app.routers.admin.tag_routes import router as tag_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Admin Auth"])
router.include_router(dashboard_router, prefix="/dashboard", tags=["Admin Dashboard"])
router.include_router(blog_router, prefix="/blogs", tags=["Admin Blogs"])
router.include_router(asset_router, prefix="/assets", tags=["Admin Assets"])
router.include_router(category_router, prefix="/categories", tags=["Admin Categories"])
router.include_router(tag_router, prefix="/tags", tags=["Admin Tags"])
router.include_router(analytics_router, prefix="/analytics", tags=["Admin Analytics"])
router.include_router(master_router, prefix="/master", tags=["Admin Master"])
