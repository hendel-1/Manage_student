from dataclasses import dataclass
from typing import Optional
from src.entities.student import Student
from src.use_cases.interfaces.student_repository import StudentRepository


@dataclass
class GetStudentInput:
    student_id: str


@dataclass
class GetStudentOutput:
    student: Optional[Student]
    found: bool
    message: str


class GetStudentUseCase:
    def __init__(self, repository: StudentRepository) -> None:
        self.repository = repository

    def execute(self, input_data: GetStudentInput) -> GetStudentOutput:
        student = self.repository.find_by_id(input_data.student_id)
        if not student:
            # Let's also check by student code if the ID doesn't match
            student = self.repository.find_by_code(input_data.student_id)

        if not student:
            return GetStudentOutput(student=None, found=False, message="Student not found")
        return GetStudentOutput(student=student, found=True, message="Student found")
