from dataclasses import dataclass
from typing import List
from src.entities.student import Student
from src.use_cases.interfaces.student_repository import StudentRepository


@dataclass
class ListStudentsInput:
    pass


@dataclass
class ListStudentsOutput:
    students: List[Student]
    total: int


class ListStudentsUseCase:
    def __init__(self, repository: StudentRepository) -> None:
        self.repository = repository

    def execute(self, input_data: ListStudentsInput) -> ListStudentsOutput:
        students = self.repository.find_all()
        return ListStudentsOutput(students=students, total=len(students))
