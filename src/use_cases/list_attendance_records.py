from dataclasses import dataclass
from typing import List, Optional
from src.entities.attendance_record import AttendanceRecord
from src.use_cases.interfaces.attendance_repository import AttendanceRepository
from src.use_cases.interfaces.student_repository import StudentRepository


@dataclass
class ListAttendanceRecordsInput:
    student_id_or_code: Optional[str] = None


@dataclass
class ListAttendanceRecordsOutput:
    records: List[AttendanceRecord]
    total: int


class ListAttendanceRecordsUseCase:
    def __init__(
        self,
        student_repository: StudentRepository,
        attendance_repository: AttendanceRepository,
    ) -> None:
        self.student_repository = student_repository
        self.attendance_repository = attendance_repository

    def execute(self, input_data: ListAttendanceRecordsInput) -> ListAttendanceRecordsOutput:
        if input_data.student_id_or_code:
            student = self.student_repository.find_by_id(input_data.student_id_or_code)
            if not student:
                student = self.student_repository.find_by_code(input_data.student_id_or_code)

            if not student:
                # If student is not found, return empty list
                return ListAttendanceRecordsOutput(records=[], total=0)

            records = self.attendance_repository.find_by_student_id(student.id)
        else:
            records = self.attendance_repository.find_all()

        return ListAttendanceRecordsOutput(records=records, total=len(records))
