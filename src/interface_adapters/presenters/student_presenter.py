from typing import Any, Dict, List
from src.entities.student import Student


class StudentPresenter:
    """
    Converts Student entities into serialisable representations (dicts) or CLI-formatted displays.
    """

    @staticmethod
    def to_dict(student: Student) -> Dict[str, Any]:
        return {
            "id": student.id,
            "student_code": student.student_code,
            "first_name": student.first_name,
            "last_name": student.last_name,
            "email": student.email,
            "created_at": student.created_at.isoformat(),
            "updated_at": student.updated_at.isoformat(),
        }

    @staticmethod
    def to_list(students: List[Student]) -> List[Dict[str, Any]]:
        return [StudentPresenter.to_dict(s) for s in students]

    @staticmethod
    def to_cli_row(student: Student) -> str:
        return f"  {student.student_code:<12}  {student.id[:8]:<10}  {student.first_name} {student.last_name:<20}  {student.email}"

    @staticmethod
    def to_cli_detail(student: Student) -> str:
        lines = [
            f"  ID           : {student.id}",
            f"  Student Code : {student.student_code}",
            f"  First Name   : {student.first_name}",
            f"  Last Name    : {student.last_name}",
            f"  Email        : {student.email}",
            f"  Created      : {student.created_at.strftime('%Y-%m-%d %H:%M')}",
            f"  Updated      : {student.updated_at.strftime('%Y-%m-%d %H:%M')}",
        ]
        return "\n".join(lines)
