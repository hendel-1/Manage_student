from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
import uuid


def _now() -> datetime:
    return datetime.now(timezone.utc)


class AttendanceStatus(Enum):
    PRESENT = "present"
    ABSENT = "absent"
    LATE = "late"
    EXCUSED = "excused"


@dataclass
class AttendanceRecord:
    """
    Entity: AttendanceRecord.
    Represents an attendance record for a student on a specific date.
    """
    student_id: str
    status: AttendanceStatus

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    date: datetime = field(default_factory=_now)
    notes: str = ""
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        if not self.student_id or not self.student_id.strip():
            raise ValueError("Student ID is required")
        if not isinstance(self.status, AttendanceStatus):
            raise ValueError(f"Invalid attendance status: {self.status}")
        self.notes = self.notes.strip()

    def update_attendance(self, status: AttendanceStatus | None = None, notes: str | None = None) -> None:
        """Update attendance status and notes."""
        if status is not None:
            if not isinstance(status, AttendanceStatus):
                raise ValueError(f"Invalid attendance status: {status}")
            self.status = status
        if notes is not None:
            self.notes = notes.strip()
        self.updated_at = _now()
