import uuid

import pytest

from src.repositories.student_repository import StudentRepository
from src.services.student_service import StudentService


@pytest.fixture
def service():
    unique_db = f"file:student_{uuid.uuid4().hex}?mode=memory&cache=shared"
    repository = StudentRepository(database_path=unique_db)
    return StudentService(repository=repository)


def test_validate_student_data_accepts_valid_student(service):
    student_data = {
        "student_id": "STU-101",
        "name": "Alice Johnson",
        "email": "alice@example.com",
        "phone": "9876543210",
        "course": "Computer Science",
        "year": "2",
        "address": "Hyderabad"
    }

    result = service.validate_student_data(student_data)

    assert result["student_id"] == "STU-101"
    assert result["name"] == "Alice Johnson"
    assert result["email"] == "alice@example.com"


def test_validate_student_data_rejects_empty_required_fields(service):
    student_data = {
        "student_id": "",
        "name": "",
        "email": "",
        "phone": "",
        "course": "",
        "year": "",
        "address": ""
    }

    with pytest.raises(ValueError, match="Please fill in all required fields"):
        service.validate_student_data(student_data)


def test_validate_student_data_rejects_invalid_email(service):
    student_data = {
        "student_id": "STU-102",
        "name": "Bob Smith",
        "email": "invalid-email",
        "phone": "9876543210",
        "course": "Mechanical",
        "year": "1",
        "address": "Pune"
    }

    with pytest.raises(ValueError, match="Please enter a valid email"):
        service.validate_student_data(student_data)


def test_dashboard_summary_contains_student_details(service):
    student_data = {
        "student_id": "STU-999",
        "name": "Dana White",
        "email": "dana@example.com",
        "phone": "9000000000",
        "course": "Arts",
        "year": "4",
        "address": "Bangalore"
    }

    service.add_student(student_data)
    summary = service.get_dashboard_summary()

    assert summary["total_students"] >= 1
    assert len(summary["all_students"]) >= 1
    assert any(student["name"] == "Dana White" for student in summary["all_students"])
