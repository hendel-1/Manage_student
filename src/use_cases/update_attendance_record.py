from dataclasses import dataclass
from src.entities.attendance_record import AttendanceRecord, AttendanceStatus
from src.use_cases.interfaces.attendance_repository import AttendanceRepository


@dataclass
class UpdateAttendanceRecordInput:
    record_id: str
    status: AttendanceStatus | None = None
    notes: str | None = None


@dataclass
class UpdateAttendanceRecordOutput:
    record: AttendanceRecord | None
    success: bool
    message: str


class UpdateAttendanceRecordUseCase:
    def __init__(self, repository: AttendanceRepository) -> None:
        self.repository = repository

    def execute(self, input_data: UpdateAttendanceRecordInput) -> UpdateAttendanceRecordOutput:
        record = self.repository.find_by_id(input_data.record_id)
        if not record:
            return UpdateAttendanceRecordOutput(record=None, success=False, message="Attendance record not found")

        try:
            record.update_attendance(status=input_data.status, notes=input_data.notes)
            updated_record = self.repository.update(record)
            return UpdateAttendanceRecordOutput(
                record=updated_record,
                success=True,
                message="Attendance record updated successfully",
            )
        except ValueError as e:
            return UpdateAttendanceRecordOutput(record=None, success=False, message=str(e))
