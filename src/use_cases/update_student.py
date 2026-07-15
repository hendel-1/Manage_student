from dataclasses import dataclass
from src.entities.student import Student
from src.use_cases.interfaces.student_repository import StudentRepository


@dataclass
class UpdateStudentInput:
    student_id: str
    student_code: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None


@dataclass
class UpdateStudentOutput:
    student: Student | None
    success: bool
    message: str


class UpdateStudentUseCase:
    def __init__(self, repository: StudentRepository) -> None:
        self.repository = repository

    def execute(self, input_data: UpdateStudentInput) -> UpdateStudentOutput:
        student = self.repository.find_by_id(input_data.student_id)
        if not student:
            return UpdateStudentOutput(student=None, success=False, message="Student not found")

        # If student_code is updated, check for conflicts with other students
        if input_data.student_code is not None and input_data.student_code.strip() != student.student_code:
            existing = self.repository.find_by_code(input_data.student_code)
            if existing and existing.id != student.id:
                return UpdateStudentOutput(
                    student=None,
                    success=False,
                    message=f"Student with code '{input_data.student_code}' already exists.",
                )

        try:
            student.update_details(
                first_name=input_data.first_name,
                last_name=input_data.last_name,
                email=input_data.email,
                student_code=input_data.student_code,
            )
            updated_student = self.repository.update(student)
            return UpdateStudentOutput(
                student=updated_student,
                success=True,
                message="Student details updated successfully",
            )
        except ValueError as e:
            return UpdateStudentOutput(student=None, success=False, message=str(e))
