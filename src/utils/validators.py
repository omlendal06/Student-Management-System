# This file contains simple validation helpers.
# These functions check whether user input is empty, valid, or in the expected format.
import re


def clean_text(value):
    """Remove extra spaces from user input for consistent validation."""
    if value is None:
        return ""
    return str(value).strip()


def is_valid_email(email):
    """Check if the email has a basic valid format."""
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, clean_text(email)))


def is_valid_phone(phone):
    """Check if the phone number contains only digits and has 10 digits."""
    cleaned = clean_text(phone)
    return cleaned.isdigit() and len(cleaned) == 10


def is_valid_student_id(student_id):
    """Student IDs should be short, clear and should not be empty."""
    cleaned = clean_text(student_id)
    return bool(cleaned) and len(cleaned) >= 3 and len(cleaned) <= 20


def has_missing_required_fields(data, required_fields):
    """Return True if any required field is empty or missing."""
    for field in required_fields:
        value = data.get(field)
        if value is None or clean_text(value) == "":
            return True
    return False
