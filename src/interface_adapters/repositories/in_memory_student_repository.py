import copy
from typing import Dict, List, Optional
from src.entities.student import Student
from src.use_cases.interfaces.student_repository import StudentRepository


class InMemoryStudentRepository(StudentRepository):
    """
    Adapter: stores students in a dict[id, Student] in memory.
    """

    def __init__(self) -> None:
        self._store: Dict[str, Student] = {}

    def save(self, student: Student) -> Student:
        if student.id in self._store:
            raise ValueError(f"Student with id '{student.id}' already exists")
        self._store[student.id] = copy.deepcopy(student)
        return copy.deepcopy(self._store[student.id])

    def find_by_id(self, student_id: str) -> Optional[Student]:
        student = self._store.get(student_id)
        return copy.deepcopy(student) if student else None

    def find_by_code(self, student_code: str) -> Optional[Student]:
        for student in self._store.values():
            if student.student_code.lower() == student_code.strip().lower():
                return copy.deepcopy(student)
        return None

    def find_all(self) -> List[Student]:
        return [copy.deepcopy(s) for s in self._store.values()]

    def update(self, student: Student) -> Student:
        if student.id not in self._store:
            raise ValueError(f"Student with id '{student.id}' not found — cannot update")
        self._store[student.id] = copy.deepcopy(student)
        return copy.deepcopy(self._store[student.id])

    def delete(self, student_id: str) -> bool:
        if student_id not in self._store:
            return False
        del self._store[student_id]
        return True
