from typing import Any, Dict
from src.interface_adapters.presenters.student_presenter import StudentPresenter
from src.use_cases.create_student import CreateStudentInput, CreateStudentUseCase
from src.use_cases.get_student import GetStudentInput, GetStudentUseCase
from src.use_cases.list_students import ListStudentsInput, ListStudentsUseCase
from src.use_cases.update_student import UpdateStudentInput, UpdateStudentUseCase
from src.use_cases.delete_student import DeleteStudentInput, DeleteStudentUseCase
from src.use_cases.interfaces.student_repository import StudentRepository
from src.use_cases.interfaces.attendance_repository import AttendanceRepository


class StudentController:
    """
    Orchestrates use cases for student-related actions.
    """

    def __init__(self, student_repository: StudentRepository, attendance_repository: AttendanceRepository) -> None:
        self.create_use_case = CreateStudentUseCase(student_repository)
        self.get_use_case = GetStudentUseCase(student_repository)
        self.list_use_case = ListStudentsUseCase(student_repository)
        self.update_use_case = UpdateStudentUseCase(student_repository)
        self.delete_use_case = DeleteStudentUseCase(student_repository, attendance_repository)

    def create_student(self, data: Dict[str, Any]) -> Dict[str, Any]:
        student_code = data.get("student_code", "").strip()
        first_name = data.get("first_name", "").strip()
        last_name = data.get("last_name", "").strip()
        email = data.get("email", "").strip()

        if not student_code or not first_name or not last_name or not email:
            return {"success": False, "error": "student_code, first_name, last_name, and email are required"}

        try:
            output = self.create_use_case.execute(
                CreateStudentInput(
                    student_code=student_code,
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                )
            )
            return {"success": True, "student": StudentPresenter.to_dict(output.student)}
        except ValueError as e:
            return {"success": False, "error": str(e)}

    def get_student(self, student_id: str) -> Dict[str, Any]:
        output = self.get_use_case.execute(GetStudentInput(student_id=student_id))
        if not output.found:
            return {"success": False, "error": output.message}
        return {"success": True, "student": StudentPresenter.to_dict(output.student)}

    def list_students(self) -> Dict[str, Any]:
        output = self.list_use_case.execute(ListStudentsInput())
        return {
            "success": True,
            "students": StudentPresenter.to_list(output.students),
            "total": output.total,
        }

    def update_student(self, student_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        output = self.update_use_case.execute(
            UpdateStudentInput(
                student_id=student_id,
                student_code=data.get("student_code"),
                first_name=data.get("first_name"),
                last_name=data.get("last_name"),
                email=data.get("email"),
            )
        )
        if not output.success:
            return {"success": False, "error": output.message}
        return {"success": True, "student": StudentPresenter.to_dict(output.student)}

    def delete_student(self, student_id: str) -> Dict[str, Any]:
        output = self.delete_use_case.execute(DeleteStudentInput(student_id=student_id))
        return {"success": output.deleted, "message": output.message}
