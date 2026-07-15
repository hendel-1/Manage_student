from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional
from src.entities.attendance_record import AttendanceRecord, AttendanceStatus
from src.use_cases.interfaces.attendance_repository import AttendanceRepository
from src.use_cases.interfaces.student_repository import StudentRepository


@dataclass
class MarkAttendanceInput:
    student_id_or_code: str
    status: AttendanceStatus
    date: Optional[datetime] = None
    notes: str = ""


@dataclass
class MarkAttendanceOutput:
    record: AttendanceRecord
    message: str = "Attendance marked successfully"


class MarkAttendanceUseCase:
    def __init__(
        self,
        student_repository: StudentRepository,
        attendance_repository: AttendanceRepository,
    ) -> None:
        self.student_repository = student_repository
        self.attendance_repository = attendance_repository

    def execute(self, input_data: MarkAttendanceInput) -> MarkAttendanceOutput:
        # Resolve student
        student = self.student_repository.find_by_id(input_data.student_id_or_code)
        if not student:
            student = self.student_repository.find_by_code(input_data.student_id_or_code)

        if not student:
            raise ValueError(f"Student '{input_data.student_id_or_code}' does not exist.")

        # Create record
        record_kwargs = {
            "student_id": student.id,
            "status": input_data.status,
            "notes": input_data.notes,
        }
        if input_data.date is not None:
            record_kwargs["date"] = input_data.date

        record = AttendanceRecord(**record_kwargs)

        # Save record
        saved_record = self.attendance_repository.save(record)

        return MarkAttendanceOutput(record=saved_record)
