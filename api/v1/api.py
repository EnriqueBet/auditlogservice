from fastapi import APIRouter
from endpoints import events, users

router = APIRouter()

router.include_router(events.router, tags=["events"], prefix="/events")
router.include_router(users.router, tags=["token"], prefix="/token")
