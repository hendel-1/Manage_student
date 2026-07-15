# Student Attendance Management System — Clean Architecture

A clean, runnable Python project that manages student attendance using **Clean Architecture** (concentric layers and the dependency rule).

---

## Architecture Diagram

```
  +------------------------------------------+
  |  FRAMEWORKS & DRIVERS                    |  Layer 4 (outermost)
  |   +--------------------------------+     |
  |   |  INTERFACE ADAPTERS           |     |
  |   |   +----------------------+   |     |
  |   |   |  USE CASES           |   |     |
  |   |   |   +--------------+   |   |     |
  |   |   |   |  ENTITIES    |   |   |     |
  |   |   |   |  (The Core)  |   |   |     |
  |   |   |   +--------------+   |   |     |
  |   |   +----------------------+   |     |
  |   +--------------------------------+     |
  +------------------------------------------+
```

### The Dependency Rule
- Dependencies can only point **inward**.
- Inner layers define **abstract interfaces** (ports).
- Outer layers implement interfaces (adapters).
- Swapping databases or delivery mechanisms requires zero business logic changes.

---

## Directory Structure

```
Manage_student/
│
├── src/
│   ├── entities/               # Layer 1 — Pure Python entities
│   │   ├── student.py
│   │   └── attendance_record.py
│   │
│   ├── use_cases/              # Layer 2 — Application logic
│   │   ├── interfaces/         # Ports (contracts)
│   │   │   ├── student_repository.py
│   │   │   └── attendance_repository.py
│   │   ├── create_student.py
│   │   ├── get_student.py
│   │   ├── list_students.py
│   │   ├── update_student.py
│   │   ├── delete_student.py
│   │   ├── mark_attendance.py
│   │   ├── get_attendance_record.py
│   │   ├── list_attendance_records.py
│   │   ├── update_attendance_record.py
│   │   └── delete_attendance_record.py
│   │
│   ├── interface_adapters/     # Layer 3 — Glue
│   │   ├── repositories/       # Adapters implementing Ports
│   │   │   ├── in_memory_student_repository.py
│   │   │   ├── sqlite_student_repository.py
│   │   │   └── sqlite_attendance_repository.py
│   │   ├── controllers/        # Framework-agnostic entry points
│   │   │   ├── student_controller.py
│   │   │   └── attendance_controller.py
│   │   └── presenters/         # Formats outputs
│   │       ├── student_presenter.py
│   │       └── attendance_presenter.py
│   │
│   └── frameworks/             # Layer 4 — Technology details
│       ├── cli/
│       │   └── cli_app.py      # Interactive CLI
│       └── web/
│           └── flask_app.py    # REST API
│
├── tests/                      # Unit & integration tests
│   ├── test_entities.py
│   ├── test_use_cases.py
│   └── test_web_api.py
│
├── main_cli.py                 # CLI entry point
├── main_web.py                 # REST API entry point
└── requirements.txt
```

---

## Getting Started

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Run Tests
```bash
pytest tests/ -v
```

### Run interactive CLI
```bash
python main_cli.py
```

### Run Web REST API
```bash
python main_web.py
```
Outputs running API at `http://localhost:5000`.

#### REST API Endpoints:
- `POST /students` : Create student
- `GET /students` : List students
- `GET /students/<id>` : Get details
- `PATCH /students/<id>` : Update details
- `DELETE /students/<id>` : Delete student (cascades to attendance logs)
- `POST /attendance` : Log attendance
- `GET /attendance` : List attendance logs (optional query filter: `?student=<id_or_code>`)
- `PATCH /attendance/<id>` : Update attendance record status/notes
- `DELETE /attendance/<id>` : Delete attendance log
