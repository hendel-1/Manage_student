from dataclasses import dataclass
from src.use_cases.interfaces.attendance_repository import AttendanceRepository


@dataclass
class DeleteAttendanceRecordInput:
    record_id: str


@dataclass
class DeleteAttendanceRecordOutput:
    deleted: bool
    message: str


class DeleteAttendanceRecordUseCase:
    def __init__(self, repository: AttendanceRepository) -> None:
        self.repository = repository

    def execute(self, input_data: DeleteAttendanceRecordInput) -> DeleteAttendanceRecordOutput:
        record = self.repository.find_by_id(input_data.record_id)
        if not record:
            return DeleteAttendanceRecordOutput(deleted=False, message="Attendance record not found")

        success = self.repository.delete(input_data.record_id)
        if success:
            return DeleteAttendanceRecordOutput(deleted=True, message="Attendance record deleted successfully")
        return DeleteAttendanceRecordOutput(deleted=False, message="Failed to delete attendance record")
