from fastapi import APIRouter

from app.api.routes import students

router = APIRouter()

router.include_router(students.router, prefix="/students", tags=["Students"])
