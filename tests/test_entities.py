import pytest
from src.entities.student import Student
from src.entities.attendance_record import AttendanceRecord, AttendanceStatus


class TestStudentValidation:
    def test_creates_with_valid_details(self):
        student = Student(
            student_code="S12345",
            first_name="John",
            last_name="Doe",
            email="john.doe@example.com",
        )
        assert student.student_code == "S12345"
        assert student.first_name == "John"
        assert student.last_name == "Doe"
        assert student.email == "john.doe@example.com"
        assert student.id is not None

    def test_strips_whitespace_from_fields(self):
        student = Student(
            student_code="  S12345  ",
            first_name="  John  ",
            last_name="  Doe  ",
            email="  john.doe@example.com  ",
        )
        assert student.student_code == "S12345"
        assert student.first_name == "John"
        assert student.last_name == "Doe"
        assert student.email == "john.doe@example.com"

    def test_raises_on_empty_code(self):
        with pytest.raises(ValueError, match="Student code cannot be empty"):
            Student(student_code="", first_name="John", last_name="Doe", email="john.doe@example.com")

    def test_raises_on_invalid_email(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            Student(student_code="S123", first_name="John", last_name="Doe", email="invalid-email")


class TestStudentUpdate:
    def test_can_update_first_name(self):
        student = Student(student_code="S123", first_name="John", last_name="Doe", email="john@example.com")
        student.update_details(first_name="Jane")
        assert student.first_name == "Jane"

    def test_update_with_invalid_email_raises(self):
        student = Student(student_code="S123", first_name="John", last_name="Doe", email="john@example.com")
        with pytest.raises(ValueError, match="Invalid email format"):
            student.update_details(email="invalid_email")


class TestAttendanceRecordValidation:
    def test_creates_with_valid_details(self):
        record = AttendanceRecord(student_id="student-123", status=AttendanceStatus.PRESENT)
        assert record.student_id == "student-123"
        assert record.status == AttendanceStatus.PRESENT
        assert record.notes == ""

    def test_raises_on_empty_student_id(self):
        with pytest.raises(ValueError, match="Student ID is required"):
            AttendanceRecord(student_id="", status=AttendanceStatus.PRESENT)

    def test_can_update_attendance(self):
        record = AttendanceRecord(student_id="student-123", status=AttendanceStatus.PRESENT)
        record.update_attendance(status=AttendanceStatus.ABSENT, notes="Sick leave")
        assert record.status == AttendanceStatus.ABSENT
        assert record.notes == "Sick leave"
