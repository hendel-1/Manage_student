from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional
from src.entities.attendance_record import AttendanceRecord, AttendanceStatus


class AttendanceRepository(ABC):
    """
    Abstract Port for AttendanceRecord persistence.
    """
    
    @abstractmethod
    def save(self, record: AttendanceRecord) -> AttendanceRecord:
        """Persist a new attendance record. Returns the saved record."""
        ...

    @abstractmethod
    def find_by_id(self, record_id: str) -> Optional[AttendanceRecord]:
        """Retrieve an attendance record by ID. Returns None if not found."""
        ...

    @abstractmethod
    def find_by_student_id(self, student_id: str) -> List[AttendanceRecord]:
        """Retrieve all attendance records for a specific student."""
        ...

    @abstractmethod
    def find_by_date(self, date: datetime) -> List[AttendanceRecord]:
        """Retrieve all attendance records for a specific date (year, month, day match)."""
        ...

    @abstractmethod
    def find_all(self) -> List[AttendanceRecord]:
        """Retrieve all attendance records."""
        ...

    @abstractmethod
    def update(self, record: AttendanceRecord) -> AttendanceRecord:
        """Persist changes to an existing attendance record. Returns the updated record."""
        ...

    @abstractmethod
    def delete(self, record_id: str) -> bool:
        """Remove an attendance record by ID. Returns True if deleted, False otherwise."""
        ...
