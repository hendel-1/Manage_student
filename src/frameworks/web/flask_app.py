from flask import Flask, jsonify, request
from src.interface_adapters.controllers.student_controller import StudentController
from src.interface_adapters.controllers.attendance_controller import AttendanceController
from src.interface_adapters.repositories.sqlite_student_repository import SQLiteStudentRepository
from src.interface_adapters.repositories.sqlite_attendance_repository import SQLiteAttendanceRepository


def create_app(student_repository=None, attendance_repository=None) -> Flask:
    """
    Application factory — creates and configures the Flask app.
    Accepts optional repositories so tests can inject in-memory ones.
    """
    app = Flask(__name__)

    # Dependency Injection
    db_path = "attendance.db"
    if student_repository is None:
        student_repository = SQLiteStudentRepository(db_path)
    if attendance_repository is None:
        attendance_repository = SQLiteAttendanceRepository(db_path)

    student_controller = StudentController(student_repository, attendance_repository)
    attendance_controller = AttendanceController(student_repository, attendance_repository)

    # Health check
    @app.get("/health")
    def health():
        return jsonify({"status": "ok"})

    # Student REST API
    @app.post("/students")
    def create_student():
        """
        Create a new student.
        Body (JSON): { "student_code": "S001", "first_name": "John", "last_name": "Doe", "email": "john.doe@example.com" }
        """
        data = request.get_json(silent=True) or {}
        result = student_controller.create_student(data)
        status_code = 201 if result["success"] else 400
        return jsonify(result), status_code

    @app.get("/students")
    def list_students():
        result = student_controller.list_students()
        return jsonify(result), 200

    @app.get("/students/<student_id>")
    def get_student(student_id: str):
        result = student_controller.get_student(student_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code

    @app.patch("/students/<student_id>")
    def update_student(student_id: str):
        """
        Update student.
        Body (JSON): { "first_name": "NewName", "email": "new.email@example.com" }
        """
        data = request.get_json(silent=True) or {}
        result = student_controller.update_student(student_id, data)
        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code

    @app.delete("/students/<student_id>")
    def delete_student(student_id: str):
        result = student_controller.delete_student(student_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code

    # Attendance REST API
    @app.post("/attendance")
    def mark_attendance():
        """
        Mark attendance.
        Body (JSON): { "student_id_or_code": "S001", "status": "present", "notes": "On time", "date": "2026-07-01" }
        """
        data = request.get_json(silent=True) or {}
        result = attendance_controller.mark_attendance(data)
        status_code = 201 if result["success"] else 400
        return jsonify(result), status_code

    @app.get("/attendance")
    def list_attendance():
        """
        List attendance records. Optional query param: ?student=student_id_or_code
        """
        student_id_or_code = request.args.get("student")
        result = attendance_controller.list_attendance_records(student_id_or_code=student_id_or_code)
        return jsonify(result), 200

    @app.get("/attendance/<record_id>")
    def get_attendance_record(record_id: str):
        result = attendance_controller.get_attendance_record(record_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code

    @app.patch("/attendance/<record_id>")
    def update_attendance_record(record_id: str):
        """
        Update attendance record status or notes.
        Body (JSON): { "status": "late", "notes": "Arrived 10 mins late" }
        """
        data = request.get_json(silent=True) or {}
        result = attendance_controller.update_attendance_record(record_id, data)
        status_code = 200 if result["success"] else 400
        return jsonify(result), status_code

    @app.delete("/attendance/<record_id>")
    def delete_attendance_record(record_id: str):
        result = attendance_controller.delete_attendance_record(record_id)
        status_code = 200 if result["success"] else 404
        return jsonify(result), status_code

    return app
