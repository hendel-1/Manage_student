import pytest
from src.entities.attendance_record import AttendanceStatus
from src.interface_adapters.repositories.in_memory_student_repository import InMemoryStudentRepository
from src.interface_adapters.repositories.in_memory_attendance_repository import InMemoryAttendanceRepository
from src.use_cases.create_student import CreateStudentInput, CreateStudentUseCase
from src.use_cases.get_student import GetStudentInput, GetStudentUseCase
from src.use_cases.list_students import ListStudentsInput, ListStudentsUseCase
from src.use_cases.update_student import UpdateStudentInput, UpdateStudentUseCase
from src.use_cases.delete_student import DeleteStudentInput, DeleteStudentUseCase
from src.use_cases.mark_attendance import MarkAttendanceInput, MarkAttendanceUseCase
from src.use_cases.get_attendance_record import GetAttendanceRecordInput, GetAttendanceRecordUseCase
from src.use_cases.list_attendance_records import ListAttendanceRecordsInput, ListAttendanceRecordsUseCase
from src.use_cases.update_attendance_record import UpdateAttendanceRecordInput, UpdateAttendanceRecordUseCase
from src.use_cases.delete_attendance_record import DeleteAttendanceRecordInput, DeleteAttendanceRecordUseCase


@pytest.fixture
def student_repo():
    return InMemoryStudentRepository()


@pytest.fixture
def attendance_repo():
    return InMemoryAttendanceRepository()


@pytest.fixture
def create_student_uc(student_repo):
    return CreateStudentUseCase(student_repo)


@pytest.fixture
def mark_attendance_uc(student_repo, attendance_repo):
    return MarkAttendanceUseCase(student_repo, attendance_repo)


class TestStudentUseCases:
    def test_creates_student_successfully(self, create_student_uc):
        output = create_student_uc.execute(
            CreateStudentInput(
                student_code="S1001",
                first_name="Alice",
                last_name="Smith",
                email="alice@example.com",
            )
        )
        assert output.student.student_code == "S1001"
        assert output.student.first_name == "Alice"
        assert output.student.id is not None

    def test_fails_on_duplicate_student_code(self, create_student_uc):
        create_student_uc.execute(
            CreateStudentInput(
                student_code="S1001",
                first_name="Alice",
                last_name="Smith",
                email="alice@example.com",
            )
        )
        with pytest.raises(ValueError, match="already exists"):
            create_student_uc.execute(
                CreateStudentInput(
                    student_code="S1001",
                    first_name="Bob",
                    last_name="Jones",
                    email="bob@example.com",
                )
            )

    def test_get_student_finds_by_id_or_code(self, student_repo, create_student_uc):
        created = create_student_uc.execute(
            CreateStudentInput(
                student_code="S1001",
                first_name="Alice",
                last_name="Smith",
                email="alice@example.com",
            )
        ).student

        get_uc = GetStudentUseCase(student_repo)

        # Find by ID
        out1 = get_uc.execute(GetStudentInput(student_id=created.id))
        assert out1.found is True
        assert out1.student.first_name == "Alice"

        # Find by Code
        out2 = get_uc.execute(GetStudentInput(student_id="S1001"))
        assert out2.found is True
        assert out2.student.id == created.id

        # Not found
        out3 = get_uc.execute(GetStudentInput(student_id="nonexistent"))
        assert out3.found is False

    def test_list_students(self, student_repo, create_student_uc):
        create_student_uc.execute(CreateStudentInput("S1", "A", "B", "a@b.com"))
        create_student_uc.execute(CreateStudentInput("S2", "C", "D", "c@d.com"))

        list_uc = ListStudentsUseCase(student_repo)
        output = list_uc.execute(ListStudentsInput())
        assert output.total == 2

    def test_update_student(self, student_repo, create_student_uc):
        created = create_student_uc.execute(CreateStudentInput("S1", "A", "B", "a@b.com")).student
        update_uc = UpdateStudentUseCase(student_repo)

        output = update_uc.execute(
            UpdateStudentInput(
                student_id=created.id,
                first_name="UpdatedName",
            )
        )
        assert output.success is True
        assert output.student.first_name == "UpdatedName"

    def test_delete_student_cascades_to_attendance(self, student_repo, attendance_repo, create_student_uc, mark_attendance_uc):
        student = create_student_uc.execute(CreateStudentInput("S1", "A", "B", "a@b.com")).student
        
        # Log attendance
        mark_attendance_uc.execute(
            MarkAttendanceInput(
                student_id_or_code=student.id,
                status=AttendanceStatus.PRESENT,
                notes="L1",
            )
        )
        
        assert len(attendance_repo.find_by_student_id(student.id)) == 1

        delete_uc = DeleteStudentUseCase(student_repo, attendance_repo)
        output = delete_uc.execute(DeleteStudentInput(student_id=student.id))
        assert output.deleted is True

        # Verify student is gone
        assert student_repo.find_by_id(student.id) is None
        # Verify attendance records are gone
        assert len(attendance_repo.find_by_student_id(student.id)) == 0


class TestAttendanceUseCases:
    def test_marks_attendance_successfully(self, create_student_uc, mark_attendance_uc):
        student = create_student_uc.execute(CreateStudentInput("S1", "A", "B", "a@b.com")).student

        output = mark_attendance_uc.execute(
            MarkAttendanceInput(
                student_id_or_code="S1",
                status=AttendanceStatus.LATE,
                notes="10m late",
            )
        )
        assert output.record.student_id == student.id
        assert output.record.status == AttendanceStatus.LATE
        assert output.record.notes == "10m late"

    def test_fails_to_mark_attendance_for_missing_student(self, mark_attendance_uc):
        with pytest.raises(ValueError, match="does not exist"):
            mark_attendance_uc.execute(
                MarkAttendanceInput(
                    student_id_or_code="nonexistent",
                    status=AttendanceStatus.PRESENT,
                )
            )

    def test_list_and_filter_attendance_records(self, student_repo, attendance_repo, create_student_uc, mark_attendance_uc):
        s1 = create_student_uc.execute(CreateStudentInput("S1", "A", "B", "a@b.com")).student
        s2 = create_student_uc.execute(CreateStudentInput("S2", "C", "D", "c@d.com")).student

        mark_attendance_uc.execute(MarkAttendanceInput(student_id_or_code="S1", status=AttendanceStatus.PRESENT))
        mark_attendance_uc.execute(MarkAttendanceInput(student_id_or_code="S2", status=AttendanceStatus.ABSENT))
        mark_attendance_uc.execute(MarkAttendanceInput(student_id_or_code="S1", status=AttendanceStatus.LATE))

        list_uc = ListAttendanceRecordsUseCase(student_repo, attendance_repo)

        # List all
        out_all = list_uc.execute(ListAttendanceRecordsInput())
        assert out_all.total == 3

        # List for S1 only
        out_s1 = list_uc.execute(ListAttendanceRecordsInput(student_id_or_code="S1"))
        assert out_s1.total == 2
