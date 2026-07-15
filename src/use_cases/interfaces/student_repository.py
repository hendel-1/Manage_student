from abc import ABC, abstractmethod
from typing import List, Optional
from src.entities.student import Student


class StudentRepository(ABC):
    """
    Abstract Port for Student persistence.
    """

    @abstractmethod
    def save(self, student: Student) -> Student:
        """Persist a new student. Returns the saved student."""
        ...

    @abstractmethod
    def find_by_id(self, student_id: str) -> Optional[Student]:
        """Retrieve a student by ID. Returns None if not found."""
        ...

    @abstractmethod
    def find_by_code(self, student_code: str) -> Optional[Student]:
        """Retrieve a student by their unique student code. Returns None if not found."""
        ...

    @abstractmethod
    def find_all(self) -> List[Student]:
        """Retrieve all students. Returns empty list if none exist."""
        ...

    @abstractmethod
    def update(self, student: Student) -> Student:
        """Persist changes to an existing student. Returns the updated student."""
        ...

    @abstractmethod
    def delete(self, student_id: str) -> bool:
        """Remove a student by ID. Returns True if deleted, False otherwise."""
        ...
