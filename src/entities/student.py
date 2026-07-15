from dataclasses import dataclass, field
from datetime import datetime, timezone
import uuid


def _now() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class Student:
    """
    Entity: Student.
    Represents a student in our system. Contains business validation.
    """
    student_code: str
    first_name: str
    last_name: str
    email: str

    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=_now)
    updated_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        self.validate()
        self.student_code = self.student_code.strip()
        self.first_name = self.first_name.strip()
        self.last_name = self.last_name.strip()
        self.email = self.email.strip()

    def validate(self) -> None:
        if not self.student_code or not self.student_code.strip():
            raise ValueError("Student code cannot be empty")
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name cannot be empty")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name cannot be empty")
        if not self.email or not self.email.strip():
            raise ValueError("Email cannot be empty")
        if "@" not in self.email or "." not in self.email:
            raise ValueError("Invalid email format")

    def update_details(
        self,
        first_name: str | None = None,
        last_name: str | None = None,
        email: str | None = None,
        student_code: str | None = None,
    ) -> None:
        """Update mutable fields with business validation."""
        if student_code is not None:
            if not student_code.strip():
                raise ValueError("Student code cannot be empty")
            self.student_code = student_code.strip()
        if first_name is not None:
            if not first_name.strip():
                raise ValueError("First name cannot be empty")
            self.first_name = first_name.strip()
        if last_name is not None:
            if not last_name.strip():
                raise ValueError("Last name cannot be empty")
            self.last_name = last_name.strip()
        if email is not None:
            if not email.strip() or "@" not in email or "." not in email:
                raise ValueError("Invalid email format")
            self.email = email.strip()
        self.updated_at = _now()
