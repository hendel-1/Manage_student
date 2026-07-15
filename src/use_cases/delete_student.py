from dataclasses import dataclass
from src.use_cases.interfaces.student_repository import StudentRepository
from src.use_cases.interfaces.attendance_repository import AttendanceRepository


@dataclass
class DeleteStudentInput:
    student_id: str


@dataclass
class DeleteStudentOutput:
    deleted: bool
    message: str


class DeleteStudentUseCase:
    def __init__(
        self,
        student_repository: StudentRepository,
        attendance_repository: AttendanceRepository,
    ) -> None:
        self.student_repository = student_repository
        self.attendance_repository = attendance_repository

    def execute(self, input_data: DeleteStudentInput) -> DeleteStudentOutput:
        student = self.student_repository.find_by_id(input_data.student_id)
        if not student:
            # Let's also check by student code
            student = self.student_repository.find_by_code(input_data.student_id)

        if not student:
            return DeleteStudentOutput(deleted=False, message="Student not found")

        # Delete all attendance records associated with the student first (cascade in application layer)
        records = self.attendance_repository.find_by_student_id(student.id)
        for record in records:
            self.attendance_repository.delete(record.id)

        # Now delete the student
        success = self.student_repository.delete(student.id)
        if success:
            return DeleteStudentOutput(
                deleted=True,
                message=f"Student '{student.first_name} {student.last_name}' and their attendance records deleted successfully",
            )
        return DeleteStudentOutput(deleted=False, message="Failed to delete student")
