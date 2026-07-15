from datetime import datetime
from typing import Any, Dict, Optional
from src.entities.attendance_record import AttendanceStatus
from src.interface_adapters.presenters.attendance_presenter import AttendancePresenter
from src.use_cases.mark_attendance import MarkAttendanceInput, MarkAttendanceUseCase
from src.use_cases.get_attendance_record import GetAttendanceRecordInput, GetAttendanceRecordUseCase
from src.use_cases.list_attendance_records import ListAttendanceRecordsInput, ListAttendanceRecordsUseCase
from src.use_cases.update_attendance_record import UpdateAttendanceRecordInput, UpdateAttendanceRecordUseCase
from src.use_cases.delete_attendance_record import DeleteAttendanceRecordInput, DeleteAttendanceRecordUseCase
from src.use_cases.interfaces.student_repository import StudentRepository
from src.use_cases.interfaces.attendance_repository import AttendanceRepository


class AttendanceController:
    """
    Orchestrates use cases for attendance-related actions.
    """

    def __init__(self, student_repository: StudentRepository, attendance_repository: AttendanceRepository) -> None:
        self.student_repository = student_repository
        self.mark_use_case = MarkAttendanceUseCase(student_repository, attendance_repository)
        self.get_use_case = GetAttendanceRecordUseCase(attendance_repository)
        self.list_use_case = ListAttendanceRecordsUseCase(student_repository, attendance_repository)
        self.update_use_case = UpdateAttendanceRecordUseCase(attendance_repository)
        self.delete_use_case = DeleteAttendanceRecordUseCase(attendance_repository)

    def mark_attendance(self, data: Dict[str, Any]) -> Dict[str, Any]:
        student_id_or_code = data.get("student_id_or_code", "").strip()
        status_str = data.get("status", "").strip().lower()

        if not student_id_or_code or not status_str:
            return {"success": False, "error": "student_id_or_code and status are required"}

        try:
            status = AttendanceStatus(status_str)
        except ValueError:
            valid_statuses = [s.value for s in AttendanceStatus]
            return {"success": False, "error": f"Invalid status. Choose from: {valid_statuses}"}

        date_val = None
        date_str = data.get("date")
        if date_str:
            try:
                # Handle standard ISO formats, e.g. YYYY-MM-DD or full ISO
                if len(date_str) == 10:
                    date_val = datetime.strptime(date_str, "%Y-%m-%d")
                else:
                    date_val = datetime.fromisoformat(date_str)
            except ValueError:
                return {"success": False, "error": "Invalid date format. Use YYYY-MM-DD or ISO 8601 format."}

        notes = data.get("notes", "")

        try:
            output = self.mark_use_case.execute(
                MarkAttendanceInput(
                    student_id_or_code=student_id_or_code,
                    status=status,
                    date=date_val,
                    notes=notes,
                )
            )
            # Resolve student info just to add detail to presentation
            student_code = ""
            student_name = ""
            student = self.student_repository.find_by_id(output.record.student_id)
            if student:
                student_code = student.student_code
                student_name = f"{student.first_name} {student.last_name}"

            record_dict = AttendancePresenter.to_dict(output.record)
            record_dict["student_code"] = student_code
            record_dict["student_name"] = student_name

            return {"success": True, "record": record_dict}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def get_attendance_record(self, record_id: str) -> Dict[str, Any]:
        output = self.get_use_case.execute(GetAttendanceRecordInput(record_id=record_id))
        if not output.found:
            return {"success": False, "error": output.message}
        
        record = output.record
        student_code = ""
        student_name = ""
        student = self.student_repository.find_by_id(record.student_id)
        if student:
            student_code = student.student_code
            student_name = f"{student.first_name} {student.last_name}"

        record_dict = AttendancePresenter.to_dict(record)
        record_dict["student_code"] = student_code
        record_dict["student_name"] = student_name
        
        return {"success": True, "record": record_dict}

    def list_attendance_records(self, student_id_or_code: Optional[str] = None) -> Dict[str, Any]:
        output = self.list_use_case.execute(ListAttendanceRecordsInput(student_id_or_code=student_id_or_code))
        
        records_formatted = []
        for record in output.records:
            student = self.student_repository.find_by_id(record.student_id)
            student_code = student.student_code if student else ""
            student_name = f"{student.first_name} {student.last_name}" if student else ""
            
            record_dict = AttendancePresenter.to_dict(record)
            record_dict["student_code"] = student_code
            record_dict["student_name"] = student_name
            records_formatted.append(record_dict)

        return {
            "success": True,
            "records": records_formatted,
            "total": output.total,
        }

    def update_attendance_record(self, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        status_str = data.get("status")
        status = None
        if status_str is not None:
            try:
                status = AttendanceStatus(status_str.strip().lower())
            except ValueError:
                valid_statuses = [s.value for s in AttendanceStatus]
                return {"success": False, "error": f"Invalid status. Choose from: {valid_statuses}"}

        notes = data.get("notes")

        output = self.update_use_case.execute(
            UpdateAttendanceRecordInput(
                record_id=record_id,
                status=status,
                notes=notes,
            )
        )
        if not output.success:
            return {"success": False, "error": output.message}
        
        record = output.record
        student_code = ""
        student_name = ""
        student = self.student_repository.find_by_id(record.student_id)
        if student:
            student_code = student.student_code
            student_name = f"{student.first_name} {student.last_name}"

        record_dict = AttendancePresenter.to_dict(record)
        record_dict["student_code"] = student_code
        record_dict["student_name"] = student_name

        return {"success": True, "record": record_dict}

    def delete_attendance_record(self, record_id: str) -> Dict[str, Any]:
        output = self.delete_use_case.execute(DeleteAttendanceRecordInput(record_id=record_id))
        return {"success": output.deleted, "message": output.message}
