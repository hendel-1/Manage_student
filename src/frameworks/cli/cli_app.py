import sys
from typing import Optional

from src.interface_adapters.controllers.student_controller import StudentController
from src.interface_adapters.controllers.attendance_controller import AttendanceController
from src.interface_adapters.presenters.student_presenter import StudentPresenter
from src.interface_adapters.presenters.attendance_presenter import AttendancePresenter
from src.interface_adapters.repositories.in_memory_student_repository import InMemoryStudentRepository
from src.interface_adapters.repositories.in_memory_attendance_repository import InMemoryAttendanceRepository


class _C:
    RESET  = "\033[0m"
    BOLD   = "\033[1m"
    GREEN  = "\033[32m"
    YELLOW = "\033[33m"
    CYAN   = "\033[36m"
    RED    = "\033[31m"


def _banner(text: str) -> None:
    print(f"\n{_C.BOLD}{_C.CYAN}{'=' * 65}{_C.RESET}")
    print(f"{_C.BOLD}{_C.CYAN}  {text}{_C.RESET}")
    print(f"{_C.BOLD}{_C.CYAN}{'=' * 65}{_C.RESET}\n")


def _ok(msg: str) -> None:
    print(f"{_C.GREEN}  ✓  {msg}{_C.RESET}")


def _err(msg: str) -> None:
    print(f"{_C.RED}  ✗  {msg}{_C.RESET}")


def run_cli() -> None:
    """
    Entry point for the interactive student attendance manager CLI.
    Uses in-memory repositories for demonstration purposes.
    """
    student_repo = InMemoryStudentRepository()
    attendance_repo = InMemoryAttendanceRepository()

    student_controller = StudentController(student_repo, attendance_repo)
    attendance_controller = AttendanceController(student_repo, attendance_repo)

    _banner("Clean Architecture Student Attendance CLI")

    while True:
        # Affichage du menu avec des numéros
        print(f"\n{_C.BOLD}--- GESTION DES ÉTUDIANTS ---{_C.RESET}")
        print("  1. Ajouter un étudiant")
        print("  2. Lister les étudiants")
        print("  3. Afficher un étudiant")
        print("  4. Modifier un étudiant")
        print("  5. Supprimer un étudiant")
        
        print(f"\n{_C.BOLD}--- GESTION DES PRÉSENCES ---{_C.RESET}")
        print("  6. Marquer une présence")
        print("  7. Lister les présences")
        print("  8. Modifier une présence")
        print("  9. Supprimer une présence")
        
        print(f"\n{_C.BOLD}--- OPTIONS ---{_C.RESET}")
        print("  0. Quitter")
        print()

        try:
            cmd = input(f"{_C.BOLD}Choisissez une option (0-9) > {_C.RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nBye!")
            break

        if cmd in ("0", "quit", "exit", "q"):
            print("Bye!")
            break

        # STUDENT COMMANDS
        elif cmd == "1":
            code = input("  Student Code : ").strip()
            first = input("  First Name   : ").strip()
            last = input("  Last Name    : ").strip()
            email = input("  Email        : ").strip()

            result = student_controller.create_student({
                "student_code": code,
                "first_name": first,
                "last_name": last,
                "email": email,
            })
            if result["success"]:
                s = result["student"]
                _ok(f"Student created: {s['first_name']} {s['last_name']} ({s['student_code']}) - ID: {s['id'][:8]}")
            else:
                _err(result["error"])

        elif cmd == "2":
            result = student_controller.list_students()
            if not result["success"]:
                _err(result["error"])
                continue
            if result["total"] == 0:
                print("  (no students)")
            else:
                print(f"  {'CODE':<12}  {'ID':<10}  {'NAME':<20}  EMAIL")
                print(f"  {'-'*65}")
                for s in result["students"]:
                    print(
                        f"  {s['student_code']:<12}  "
                        f"{s['id'][:8]:<10}  "
                        f"{s['first_name'] + ' ' + s['last_name']:<20}  "
                        f"{s['email']}"
                    )
                print(f"\n  Total: {result['total']}")

        elif cmd == "3":
            student_id = input("  Student ID or Code: ").strip()
            result = student_controller.get_student(student_id)
            if not result["success"]:
                _err(result["error"])
            else:
                s = result["student"]
                print(f"\n  ID           : {s['id']}")
                print(f"  Student Code : {s['student_code']}")
                print(f"  First Name   : {s['first_name']}")
                print(f"  Last Name    : {s['last_name']}")
                print(f"  Email        : {s['email']}")
                print(f"  Created      : {s['created_at'][:19]}")

        elif cmd == "4":
            student_id = input("  Student ID: ").strip()
            code = input("  New Student Code (leave blank to keep): ").strip() or None
            first = input("  New First Name (leave blank to keep): ").strip() or None
            last = input("  New Last Name (leave blank to keep): ").strip() or None
            email = input("  New Email (leave blank to keep): ").strip() or None

            data = {}
            if code: data["student_code"] = code
            if first: data["first_name"] = first
            if last: data["last_name"] = last
            if email: data["email"] = email

            result = student_controller.update_student(student_id, data)
            if result["success"]:
                s = result["student"]
                _ok(f"Updated: {s['first_name']} {s['last_name']} ({s['student_code']})")
            else:
                _err(result["error"])

        elif cmd == "5":
            student_id = input("  Student ID or Code: ").strip()
            result = student_controller.delete_student(student_id)
            if result["success"]:
                _ok(result["message"])
            else:
                _err(result["message"])

        # ATTENDANCE COMMANDS
        elif cmd == "6":
            student_ref = input("  Student ID or Code: ").strip()
            status = input("  Status (present, absent, late, excused): ").strip().lower()
            notes = input("  Notes (optional): ").strip()
            date = input("  Date (YYYY-MM-DD, optional): ").strip() or None

            data = {
                "student_id_or_code": student_ref,
                "status": status,
                "notes": notes,
            }
            if date:
                data["date"] = date

            result = attendance_controller.mark_attendance(data)
            if result["success"]:
                r = result["record"]
                _ok(f"Attendance marked as '{r['status'].upper()}' for {r['student_name']}")
            else:
                _err(result["error"])

        elif cmd == "7":
            student_ref = input("  Filter by Student ID or Code (leave blank for all): ").strip() or None
            result = attendance_controller.list_attendance_records(student_id_or_code=student_ref)
            if not result["success"]:
                _err(result["error"])
                continue
            if result["total"] == 0:
                print("  (no attendance records)")
            else:
                print(f"  {'DATE & TIME':<17}  {'STUDENT':<30}  {'STATUS':<10}  NOTES")
                print(f"  {'-'*65}")
                for r in result["records"]:
                    status_disp = r["status"].upper()
                    student_disp = f"{r['student_name']} ({r['student_code']})"
                    date_disp = r["date"][:16].replace("T", " ")
                    print(
                        f"  {date_disp:<17}  "
                        f"{student_disp:<30}  "
                        f"{status_disp:<10}  "
                        f"{r['notes']}"
                    )
                print(f"\n  Total: {result['total']}")

        elif cmd == "8":
            record_id = input("  Attendance Record ID: ").strip()
            status = input("  New Status (present, absent, late, excused, leave blank to keep): ").strip().lower() or None
            notes = input("  New Notes (leave blank to keep): ").strip() or None

            data = {}
            if status: data["status"] = status
            if notes is not None: data["notes"] = notes

            result = attendance_controller.update_attendance_record(record_id, data)
            if result["success"]:
                r = result["record"]
                _ok(f"Attendance updated for {r['student_name']} -> {r['status'].upper()}")
            else:
                _err(result["error"])

        elif cmd == "9":
            record_id = input("  Attendance Record ID: ").strip()
            result = attendance_controller.delete_attendance_record(record_id)
            if result["success"]:
                _ok(result["message"])
            else:
                _err(result["message"])

        else:
            print(f"  {_C.RED}Option invalide : '{cmd}'{_C.RESET}")
            print("  Veuillez entrer un chiffre entre 0 et 9 correspondant aux choix ci-dessus.")