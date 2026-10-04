# This file contains the business rules of the application.
# The service layer checks user input and decides whether an action is allowed.
from src.repositories.student_repository import StudentRepository
from src.utils.validators import clean_text, has_missing_required_fields, is_valid_email, is_valid_phone, is_valid_student_id


class StudentService:
    """Handles validation and business logic for student operations."""

    # These are the required fields every student record must have.
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
        """Store a repository object. If no repository is given, use the default database repository."""
        self.repository = repository or StudentRepository()

    def validate_student_data(self, student_data):
        """Clean and validate student data before saving it to the database."""
        if not student_data or has_missing_required_fields(student_data, self.REQUIRED_FIELDS):
            raise ValueError("Please fill in all required fields.")

        # Clean the incoming data so spaces and blank values are handled properly.
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

    def get_course_distribution(self, students=None):
        """Build course totals for analytics cards and charts."""
        student_list = students if students is not None else self.repository.get_all_students()
        if not student_list:
            return []

        counts = {}
        for student in student_list:
            course_name = clean_text(student.get("course", ""))
            if not course_name:
                continue
            counts[course_name] = counts.get(course_name, 0) + 1

        total_students = sum(counts.values())
        result = []
        for course, count in sorted(counts.items(), key=lambda item: (-item[1], item[0])):
            result.append({
                "course": course,
                "count": count,
                "percentage": round((count / total_students) * 100, 1) if total_students else 0,
            })
        return result

    def get_year_distribution(self, students=None):
        """Summarize student counts by year for charts."""
        student_list = students if students is not None else self.repository.get_all_students()
        year_counts = {}
        for student in student_list:
            year = clean_text(student.get("year", ""))
            if not year:
                continue
            year_counts[year] = year_counts.get(year, 0) + 1

        distribution = []
        for year, count in sorted(year_counts.items(), key=lambda item: item[0]):
            distribution.append({"label": f"Year {year}", "value": count})
        return distribution

    def get_recent_notifications(self, recent_students=None):
        """Create a list of real notifications from recent student records."""
        students = recent_students if recent_students is not None else self.repository.get_recent_students(limit=3)
        notifications = []
        for student in students[:3]:
            notifications.append({
                "title": "New student added",
                "message": f"{student.get('name', 'Student')} enrolled in {student.get('course', 'the program')}",
            })

        if not notifications:
            notifications.append({
                "title": "System ready",
                "message": "No students have been added yet.",
            })

        return notifications

    def get_dashboard_summary(self):
        """Return summary values and detailed student records for the dashboard."""
        all_students = self.repository.get_all_students()
        total_students = len(all_students)
        total_courses = len({student.get("course", "") for student in all_students if student.get("course")})
        recent_students = self.repository.get_recent_students(limit=5)
        new_students = len(recent_students)
        active_students = total_students if total_students else 0
        active_percentage = round((active_students / total_students) * 100, 1) if total_students else 0

        return {
            "total_students": total_students,
            "total_courses": total_courses,
            "new_students": new_students,
            "active_students": active_students,
            "active_percentage": active_percentage,
            "recent_students": recent_students,
            "all_students": all_students,
            "course_distribution": self.get_course_distribution(all_students),
            "year_distribution": self.get_year_distribution(all_students),
            "notifications": self.get_recent_notifications(recent_students),
        }
