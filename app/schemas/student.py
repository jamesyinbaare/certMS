import typing

from pydantic import BaseModel


class Student(BaseModel):
    name: str
    student_id: str
    programme: str
    school: str
    cert_id: typing.Optional[str]
