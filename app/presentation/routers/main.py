# app/presentation/routers/main.py

from dishka.integrations.fastapi import DishkaRoute
from fastapi import APIRouter

from .auth import router as auth_router
from .media import router as media_router
from .moto_club import router as moto_club_router
from .motorcycle import router as motorcycle_router
from .profile import router as profile_router
from .user import router as user_router

__all__ = ["router"]


router = APIRouter(route_class=DishkaRoute)
router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(user_router, prefix="/users", tags=["Users"])
router.include_router(motorcycle_router, prefix="/motorcycle", tags=["Motorcycle"])
router.include_router(profile_router, prefix="/profile", tags=["Profile"])
router.include_router(media_router, prefix="/media", tags=["Media"])
router.include_router(moto_club_router, prefix="/moto-club", tags=["Moto Club"])

