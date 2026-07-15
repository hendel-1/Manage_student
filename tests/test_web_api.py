import pytest
from src.frameworks.web.flask_app import create_app
from src.interface_adapters.repositories.in_memory_student_repository import InMemoryStudentRepository
from src.interface_adapters.repositories.in_memory_attendance_repository import InMemoryAttendanceRepository


@pytest.fixture
def client():
    student_repo = InMemoryStudentRepository()
    attendance_repo = InMemoryAttendanceRepository()
    app = create_app(
        student_repository=student_repo,
        attendance_repository=attendance_repo,
    )
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def _post_student(client, student_code="S001", first_name="John", last_name="Doe", email="john.doe@example.com"):
    return client.post(
        "/students",
        json={
            "student_code": student_code,
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        },
    )


class TestStudentAPI:
    def test_creates_student_returns_201(self, client):
        res = _post_student(client, "S001", "Alice", "Smith", "alice@example.com")
        assert res.status_code == 201
        data = res.get_json()
        assert data["success"] is True
        assert data["student"]["first_name"] == "Alice"
        assert data["student"]["student_code"] == "S001"

    def test_duplicate_student_code_returns_400(self, client):
        _post_student(client, "S001", "Alice", "Smith", "alice@example.com")
        res = _post_student(client, "S001", "Bob", "Jones", "bob@example.com")
        assert res.status_code == 400
        assert res.get_json()["success"] is False
        assert "already exists" in res.get_json()["error"]

    def test_get_student_returns_details(self, client):
        created = _post_student(client, "S001").get_json()["student"]
        res = client.get(f"/students/{created['id']}")
        assert res.status_code == 200
        assert res.get_json()["student"]["student_code"] == "S001"

    def test_update_student_returns_200(self, client):
        created = _post_student(client, "S001").get_json()["student"]
        res = client.patch(f"/students/{created['id']}", json={"first_name": "Jane"})
        assert res.status_code == 200
        assert res.get_json()["student"]["first_name"] == "Jane"

    def test_delete_student_cascades(self, client):
        created = _post_student(client, "S001").get_json()["student"]
        
        # Log attendance
        client.post(
            "/attendance",
            json={"student_id_or_code": "S001", "status": "present", "notes": "Class A"},
        )

        # Verify attendance list has 1 record
        assert client.get("/attendance?student=S001").get_json()["total"] == 1

        # Delete student
        res = client.delete(f"/students/{created['id']}")
        assert res.status_code == 200
        assert res.get_json()["success"] is True

        # Verify student is gone (404)
        assert client.get(f"/students/{created['id']}").status_code == 404
        # Verify attendance record is gone
        assert client.get("/attendance?student=S001").get_json()["total"] == 0


class TestAttendanceAPI:
    def test_mark_attendance_returns_201(self, client):
        _post_student(client, "S001", "Alice", "Smith", "alice@example.com")
        res = client.post(
            "/attendance",
            json={"student_id_or_code": "S001", "status": "present", "notes": "On time"},
        )
        assert res.status_code == 201
        data = res.get_json()
        assert data["success"] is True
        assert data["record"]["status"] == "present"
        assert data["record"]["student_name"] == "Alice Smith"

    def test_mark_attendance_for_invalid_student_returns_400(self, client):
        res = client.post(
            "/attendance",
            json={"student_id_or_code": "invalid", "status": "present"},
        )
        assert res.status_code == 400
        assert res.get_json()["success"] is False
        assert "does not exist" in res.get_json()["error"]
