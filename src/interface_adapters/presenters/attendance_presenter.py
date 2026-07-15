from typing import Any, Dict, List
from src.entities.attendance_record import AttendanceRecord


class AttendancePresenter:
    """
    Converts AttendanceRecord entities into serialisable representations (dicts) or CLI-formatted displays.
    """

    @staticmethod
    def to_dict(record: AttendanceRecord) -> Dict[str, Any]:
        return {
            "id": record.id,
            "student_id": record.student_id,
            "date": record.date.isoformat(),
            "status": record.status.value,
            "notes": record.notes,
            "created_at": record.created_at.isoformat(),
            "updated_at": record.updated_at.isoformat(),
        }

    @staticmethod
    def to_list(records: List[AttendanceRecord]) -> List[Dict[str, Any]]:
        return [AttendancePresenter.to_dict(r) for r in records]

    @staticmethod
    def to_cli_row(record: AttendanceRecord, student_code: str = "", student_name: str = "") -> str:
        date_str = record.date.strftime("%Y-%m-%d %H:%M")
        status_disp = record.status.value.upper()
        student_disp = f"{student_name} ({student_code})" if student_name else record.student_id[:8]
        return f"  {date_str:<17}  {student_disp:<30}  {status_disp:<10}  {record.notes[:30]}"

    @staticmethod
    def to_cli_detail(record: AttendanceRecord, student_code: str = "", student_name: str = "") -> str:
        lines = [
            f"  Record ID    : {record.id}",
            f"  Student Name : {student_name or '(unknown)'}",
            f"  Student Code : {student_code or '(unknown)'}",
            f"  Student ID   : {record.student_id}",
            f"  Date & Time  : {record.date.strftime('%Y-%m-%d %H:%M:%S')}",
            f"  Status       : {record.status.value.upper()}",
            f"  Notes        : {record.notes or '(none)'}",
            f"  Created      : {record.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"  Updated      : {record.updated_at.strftime('%Y-%m-%d %H:%M')}",
        ]
        return "\n".join(lines)
