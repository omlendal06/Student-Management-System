from dataclasses import dataclass


@dataclass
class Student:
    """Represents a single student record in the application."""

    student_id: str
    name: str
    email: str
    phone: str
    course: str
    year: str
    address: str

    def to_dict(self):
        """Convert the student object into a dictionary for storage or display."""
        return {
            "student_id": self.student_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "course": self.course,
            "year": self.year,
            "address": self.address,
        }
