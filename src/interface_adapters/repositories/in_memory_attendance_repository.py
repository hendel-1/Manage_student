import copy
from datetime import datetime
from typing import Dict, List, Optional
from src.entities.attendance_record import AttendanceRecord
from src.use_cases.interfaces.attendance_repository import AttendanceRepository


class InMemoryAttendanceRepository(AttendanceRepository):
    """
    Adapter: stores attendance records in a dict[id, AttendanceRecord] in memory.
    """

    def __init__(self) -> None:
        self._store: Dict[str, AttendanceRecord] = {}

    def save(self, record: AttendanceRecord) -> AttendanceRecord:
        if record.id in self._store:
            raise ValueError(f"Attendance record with id '{record.id}' already exists")
        self._store[record.id] = copy.deepcopy(record)
        return copy.deepcopy(self._store[record.id])

    def find_by_id(self, record_id: str) -> Optional[AttendanceRecord]:
        record = self._store.get(record_id)
        return copy.deepcopy(record) if record else None

    def find_by_student_id(self, student_id: str) -> List[AttendanceRecord]:
        return [
            copy.deepcopy(r)
            for r in self._store.values()
            if r.student_id == student_id
        ]

    def find_by_date(self, date: datetime) -> List[AttendanceRecord]:
        return [
            copy.deepcopy(r)
            for r in self._store.values()
            if r.date.date() == date.date()
        ]

    def find_all(self) -> List[AttendanceRecord]:
        return [copy.deepcopy(r) for r in self._store.values()]

    def update(self, record: AttendanceRecord) -> AttendanceRecord:
        if record.id not in self._store:
            raise ValueError(f"Attendance record with id '{record.id}' not found — cannot update")
        self._store[record.id] = copy.deepcopy(record)
        return copy.deepcopy(self._store[record.id])

    def delete(self, record_id: str) -> bool:
        if record_id not in self._store:
            return False
        del self._store[record_id]
        return True
