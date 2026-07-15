import sqlite3
from datetime import datetime, timezone
from typing import List, Optional

from src.entities.attendance_record import AttendanceRecord, AttendanceStatus
from src.use_cases.interfaces.attendance_repository import AttendanceRepository

_DT_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"


class SQLiteAttendanceRepository(AttendanceRepository):
    """
    Adapter: persists attendance records to a SQLite database file.
    """

    def __init__(self, db_path: str = "attendance.db") -> None:
        self.db_path = db_path
        self._init_schema()

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS attendance_records (
                    id         TEXT PRIMARY KEY,
                    student_id TEXT NOT NULL,
                    date       TEXT NOT NULL,
                    status     TEXT NOT NULL,
                    notes      TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

    def save(self, record: AttendanceRecord) -> AttendanceRecord:
        with self._connect() as conn:
            conn.execute(
                """
                INSERT INTO attendance_records (id, student_id, date, status, notes, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                self._to_row(record),
            )
        return record

    def find_by_id(self, record_id: str) -> Optional[AttendanceRecord]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM attendance_records WHERE id = ?", (record_id,))
            row = cursor.fetchone()
        return self._from_row(row) if row else None

    def find_by_student_id(self, student_id: str) -> List[AttendanceRecord]:
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM attendance_records WHERE student_id = ? ORDER BY date DESC",
                (student_id,),
            )
            rows = cursor.fetchall()
        return [self._from_row(r) for r in rows]

    def find_by_date(self, date: datetime) -> List[AttendanceRecord]:
        # Perform date matching on the date portion (YYYY-MM-DD)
        date_str = date.strftime("%Y-%m-%d") + "%"
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT * FROM attendance_records WHERE date LIKE ? ORDER BY date DESC",
                (date_str,),
            )
            rows = cursor.fetchall()
        return [self._from_row(r) for r in rows]

    def find_all(self) -> List[AttendanceRecord]:
        with self._connect() as conn:
            cursor = conn.execute("SELECT * FROM attendance_records ORDER BY date DESC")
            rows = cursor.fetchall()
        return [self._from_row(r) for r in rows]

    def update(self, record: AttendanceRecord) -> AttendanceRecord:
        with self._connect() as conn:
            conn.execute(
                """
                UPDATE attendance_records
                SET status = ?, notes = ?, updated_at = ?
                WHERE id = ?
                """,
                (
                    record.status.value,
                    record.notes,
                    record.updated_at.strftime(_DT_FORMAT),
                    record.id,
                ),
            )
        return record

    def delete(self, record_id: str) -> bool:
        with self._connect() as conn:
            cursor = conn.execute("DELETE FROM attendance_records WHERE id = ?", (record_id,))
        return cursor.rowcount > 0

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _to_row(self, record: AttendanceRecord) -> tuple:
        return (
            record.id,
            record.student_id,
            record.date.strftime(_DT_FORMAT),
            record.status.value,
            record.notes,
            record.created_at.strftime(_DT_FORMAT),
            record.updated_at.strftime(_DT_FORMAT),
        )

    def _from_row(self, row: sqlite3.Row) -> AttendanceRecord:
        return AttendanceRecord(
            id=row["id"],
            student_id=row["student_id"],
            date=datetime.strptime(row["date"], _DT_FORMAT).replace(tzinfo=timezone.utc),
            status=AttendanceStatus(row["status"]),
            notes=row["notes"],
            created_at=datetime.strptime(row["created_at"], _DT_FORMAT).replace(tzinfo=timezone.utc),
            updated_at=datetime.strptime(row["updated_at"], _DT_FORMAT).replace(tzinfo=timezone.utc),
        )
