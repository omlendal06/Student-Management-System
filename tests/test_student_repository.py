from src.repositories.student_repository import StudentRepository


def test_repository_create_and_fetch_student():
    repository = StudentRepository(database_path=':memory:')

    student = {
        "student_id": "STU-200",
        "name": "Charlie Brown",
        "email": "charlie@example.com",
        "phone": "9988776655",
        "course": "Biology",
        "year": "3",
        "address": "Delhi"
    }

    repository.create_student(student)
    fetched_student = repository.get_student_by_id("STU-200")

    assert fetched_student is not None
    assert fetched_student["name"] == "Charlie Brown"
    assert fetched_student["course"] == "Biology"
