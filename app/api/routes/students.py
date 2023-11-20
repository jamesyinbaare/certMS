from fastapi import APIRouter, HTTPException, status

from app import schemas
from app.models import Student

router = APIRouter()


@router.post("/", response_model=schemas.Student, status_code=status.HTTP_201_CREATED)
async def create_student(student: schemas.Student) -> Student:
    """Create new student in the database."""
    user = await Student.get_by_student_id(student_id=student.student_id)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The student associated with this student_id already exists",
        )
    data = student.dict()
    return await Student(**data).insert()


@router.get("/", response_model=schemas.Student, status_code=status.HTTP_200_OK)
async def get_student(student_id: str) -> Student:
    """Create new student in the database."""
    student = await Student.get_by_student_id(student_id=student_id)
    if not student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The student associated with this student_id does not exists",
        )

    return student
