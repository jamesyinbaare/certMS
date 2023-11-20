import typing

from beanie import Document, Indexed


class Student(Document):
    name: str
    student_id: Indexed(str, unique=True)
    programme: str
    school: str
    cert_id: typing.Optional[str]

    @classmethod
    async def get_by_student_id(cls, *, student_id: str) -> typing.Optional["Student"]:
        return await cls.find_one(cls.student_id == student_id)
