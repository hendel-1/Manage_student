from dataclasses import dataclass
from typing import Optional
from src.entities.attendance_record import AttendanceRecord
from src.use_cases.interfaces.attendance_repository import AttendanceRepository


@dataclass
class GetAttendanceRecordInput:
    record_id: str


@dataclass
class GetAttendanceRecordOutput:
    record: Optional[AttendanceRecord]
    found: bool
    message: str


class GetAttendanceRecordUseCase:
    def __init__(self, repository: AttendanceRepository) -> None:
        self.repository = repository

    def execute(self, input_data: GetAttendanceRecordInput) -> GetAttendanceRecordOutput:
        record = self.repository.find_by_id(input_data.record_id)
        if not record:
            return GetAttendanceRecordOutput(record=None, found=False, message="Attendance record not found")
        return GetAttendanceRecordOutput(record=record, found=True, message="Attendance record found")
