import sqlite3
from datetime import datetime, timezone
from typing import List, Optional

from src.entities.student import Student
from src.use_cases.interfaces.student_repository import StudentRepository

_DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class SQLiteStudentRepository(StudentRepository):
    """
    Adapter: persists students to a SQLite database file.
    """

    def __init__(self, db_path: str = "attendance.db") -> None:
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS students (
                    id           TEXT PRIMARY KEY,
                    student_code TEXT UNIQUE NOT NULL,
                    first_name   TEXT NOT NULL,
                    last_name    TEXT NOT NULL,
                    email        TEXT NOT NULL,
                    created_at   TEXT NOT NULL,
                    updated_at   TEXT NOT NULL
                )
            """)

    def save(self, student: Student) -> Student:
        with self._connect() as conn:
            try:
                conn.execute(
                    """
                    INSERT INTO students (id, student_code, first_name, last_name, email, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    self._to_row(student),
                )
            except sqlite3.IntegrityError as e:
                # Raise ValueError for consistency with in-memory store
                if "student_code" in str(e):
                    raise ValueError(f"Student with code '{student.student_code}' already exists")
                raise e
        return student

    def find_by_id(self, student_id: str) -> Optional[Student]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM students WHERE id = ?", (student_id,))
            row = cursor.fetchone()
        return self._from_row(row) if row else None

    def find_by_code(self, student_code: str) -> Optional[Student]:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM students WHERE LOWER(student_code) = ?",
                (student_code.strip().lower(),),
            )
            row = cursor.fetchone()
        return self._from_row(row) if row else None

    def find_all(self) -> List[Student]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM students")
            rows = cursor.fetchall()
        return [self._from_row(r) for r in rows]

    def update(self, student: Student) -> Student:
        with self._connect() as conn:
            try:
                conn.execute(
                    """
                    UPDATE students
                    SET student_code = ?, first_name = ?, last_name = ?, email = ?, updated_at = ?
                    WHERE id = ?
                    """,
                    (
                        student.student_code,
                        student.first_name,
                        student.last_name,
                        student.email,
                        student.updated_at.strftime(_DT_FORMAT),
                        student.id,
                    ),
                )
            except sqlite3.IntegrityError as e:
                if "student_code" in str(e):
                    raise ValueError(f"Student with code '{student.student_code}' already exists")
                raise e
        return student

    def delete(self, student_id: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM students WHERE id = ?", (student_id,))
        return cursor.rowcount > 0

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _to_row(self, student: Student) -> tuple:
        return (
            student.id,
            student.student_code,
            student.first_name,
            student.last_name,
            student.email,
            student.created_at.strftime(_DT_FORMAT),
            student.updated_at.strftime(_DT_FORMAT),
        )

    def _from_row(self, row: sqlite3.Row) -> Student:
        return Student(
            id=row["id"],
            student_code=row["student_code"],
            first_name=row["first_name"],
            last_name=row["last_name"],
            email=row["email"],
            created_at=datetime.strptime(row["created_at"], _DT_FORMAT).replace(tzinfo=timezone.utc),
            updated_at=datetime.strptime(row["updated_at"], _DT_FORMAT).replace(tzinfo=timezone.utc),
        )
