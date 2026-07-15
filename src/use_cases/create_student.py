from dataclasses import dataclass
from src.entities.student import Student
from src.use_cases.interfaces.student_repository import StudentRepository


@dataclass
class CreateStudentInput:
    student_code: str
    first_name: str
    last_name: str
    email: str


@dataclass
class CreateStudentOutput:
    student: Student
    message: str = "Student created successfully"


class CreateStudentUseCase:
    def __init__(self, repository: StudentRepository) -> None:
        self.repository = repository

    def execute(self, input_data: CreateStudentInput) -> CreateStudentOutput:
        # Check if student code already exists (Business Rule: Student code must be unique)
        existing = self.repository.find_by_code(input_data.student_code)
        if existing:
            raise ValueError(f"Student with code '{input_data.student_code}' already exists.")

        student = Student(
            student_code=input_data.student_code,
            first_name=input_data.first_name,
            last_name=input_data.last_name,
            email=input_data.email,
        )
        saved_student = self.repository.save(student)
        return CreateStudentOutput(student=saved_student)
