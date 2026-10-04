from src.repositories.student_repository import StudentRepository
from src.utils.validators import clean_text, has_missing_required_fields, is_valid_email, is_valid_phone, is_valid_student_id


class StudentService:
    """Handles validation and business logic for student operations."""

    REQUIRED_FIELDS = [
        "student_id",
        "name",
        "email",
        "phone",
        "course",
        "year",
        "address",
    ]

    def __init__(self, repository=None):
        self.repository = repository or StudentRepository()

    def validate_student_data(self, student_data):
        """Clean and validate student data before storing it in the database."""
        if not student_data or has_missing_required_fields(student_data, self.REQUIRED_FIELDS):
            raise ValueError("Please fill in all required fields.")

        cleaned_data = {
            "student_id": clean_text(student_data.get("student_id")),
            "name": clean_text(student_data.get("name")),
            "email": clean_text(student_data.get("email")),
            "phone": clean_text(student_data.get("phone")),
            "course": clean_text(student_data.get("course")),
            "year": clean_text(student_data.get("year")),
            "address": clean_text(student_data.get("address")),
        }

        if not is_valid_student_id(cleaned_data["student_id"]):
            raise ValueError("Please enter a valid student ID.")

        if self.repository.get_student_by_id(cleaned_data["student_id"]) is not None:
            raise ValueError("Student ID already exists.")

        if not cleaned_data["name"]:
            raise ValueError("Please fill in all required fields.")

        if not is_valid_email(cleaned_data["email"]):
            raise ValueError("Please enter a valid email.")

        if not is_valid_phone(cleaned_data["phone"]):
            raise ValueError("Please enter a valid phone number.")

        if not cleaned_data["course"]:
            raise ValueError("Please fill in all required fields.")

        if not cleaned_data["year"].isdigit():
            raise ValueError("Please enter a valid year.")

        if not cleaned_data["address"]:
            raise ValueError("Please fill in all required fields.")

        return cleaned_data

    def add_student(self, student_data):
        """Validate and save a new student."""
        cleaned_data = self.validate_student_data(student_data)
        return self.repository.create_student(cleaned_data)

    def get_all_students(self):
        """Return all student records."""
        return self.repository.get_all_students()

    def get_student_by_id(self, student_id):
        """Fetch one student using the student ID."""
        student = self.repository.get_student_by_id(student_id)
        if student is None:
            raise ValueError("Student not found.")
        return student

    def update_student(self, student_id, student_data):
        """Update a student's information after checking validation."""
        existing_student = self.repository.get_student_by_id(student_id)
        if existing_student is None:
            raise ValueError("Student not found.")

        if not student_data or has_missing_required_fields(student_data, self.REQUIRED_FIELDS):
            raise ValueError("Please fill in all required fields.")

        cleaned_data = {
            "student_id": clean_text(student_data.get("student_id", student_id)),
            "name": clean_text(student_data.get("name")),
            "email": clean_text(student_data.get("email")),
            "phone": clean_text(student_data.get("phone")),
            "course": clean_text(student_data.get("course")),
            "year": clean_text(student_data.get("year")),
            "address": clean_text(student_data.get("address")),
        }

        if not is_valid_student_id(cleaned_data["student_id"]):
            raise ValueError("Please enter a valid student ID.")

        if cleaned_data["student_id"] != student_id:
            duplicate_student = self.repository.get_student_by_id(cleaned_data["student_id"])
            if duplicate_student is not None:
                raise ValueError("Student ID already exists.")

        if not is_valid_email(cleaned_data["email"]):
            raise ValueError("Please enter a valid email.")

        if not is_valid_phone(cleaned_data["phone"]):
            raise ValueError("Please enter a valid phone number.")

        if not cleaned_data["year"].isdigit():
            raise ValueError("Please enter a valid year.")

        self.repository.update_student(student_id, cleaned_data)
        return cleaned_data

    def delete_student(self, student_id):
        """Delete a student if it exists."""
        if self.repository.get_student_by_id(student_id) is None:
            raise ValueError("Student not found.")
        self.repository.delete_student(student_id)

    def search_students(self, keyword):
        """Search by name, student ID, email, or course."""
        keyword = clean_text(keyword)
        if not keyword:
            return self.repository.get_all_students()
        return self.repository.search_students(keyword)

    def get_dashboard_summary(self):
        """Return summary values and detailed student records for the dashboard."""
        total_students = self.repository.count_students()
        total_courses = self.repository.count_courses()
        recent_students = self.repository.get_recent_students(limit=5)
        all_students = self.repository.get_all_students()
        return {
            "total_students": total_students,
            "total_courses": total_courses,
            "recent_students": recent_students,
            "all_students": all_students,
        }
