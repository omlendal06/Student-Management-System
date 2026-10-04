# This repository layer is responsible for all database operations.
# It talks directly to SQLite and keeps the rest of the project cleaner.
import sqlite3

from src.utils.database import DEFAULT_DATABASE_PATH, initialize_database, load_schema_sql


class StudentRepository:
    """This class handles all database actions related to students."""

    def __init__(self, database_path=None):
        """Choose a normal file database or an in-memory database for tests."""
        if database_path == ":memory:":
            self.database_path = "file:student_management_memory?mode=memory&cache=shared"
        else:
            self.database_path = database_path or DEFAULT_DATABASE_PATH
        initialize_database(self.database_path)

    def _connect(self):
        """Create a database connection and return a row-based connection."""
        connection = sqlite3.connect(self.database_path, uri=self.database_path.startswith("file:"))
        connection.row_factory = sqlite3.Row

        # For in-memory SQLite databases, we need to apply the schema again
        # on each new connection so every connection sees the same tables.
        if self.database_path.startswith("file:"):
            connection.executescript(load_schema_sql())

        return connection

    def create_student(self, student_data):
        """Insert a student record into the database."""
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO students (student_id, name, email, phone, course, year, address)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    student_data["student_id"],
                    student_data["name"],
                    student_data["email"],
                    student_data["phone"],
                    student_data["course"],
                    student_data["year"],
                    student_data["address"],
                ),
            )
            return cursor.lastrowid

    def get_all_students(self):
        """Return all students sorted by name."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM students ORDER BY name ASC"
            ).fetchall()
            return [dict(row) for row in rows]

    def get_student_by_id(self, student_id):
        """Fetch one student using the student ID."""
        with self._connect() as connection:
            row = connection.execute(
                "SELECT * FROM students WHERE student_id = ?",
                (student_id,),
            ).fetchone()
            return dict(row) if row else None

    def update_student(self, student_id, student_data):
        """Update an existing student record."""
        with self._connect() as connection:
            connection.execute(
                """
                UPDATE students
                SET name = ?, email = ?, phone = ?, course = ?, year = ?, address = ?
                WHERE student_id = ?
                """,
                (
                    student_data["name"],
                    student_data["email"],
                    student_data["phone"],
                    student_data["course"],
                    student_data["year"],
                    student_data["address"],
                    student_id,
                ),
            )

    def delete_student(self, student_id):
        """Delete a student record using the student ID."""
        with self._connect() as connection:
            cursor = connection.execute(
                "DELETE FROM students WHERE student_id = ?",
                (student_id,),
            )
            return cursor.rowcount

    def search_students(self, keyword):
        """Search students by name, email, course, or student_id."""
        with self._connect() as connection:
            rows = connection.execute(
                """
                SELECT * FROM students
                WHERE student_id LIKE ?
                   OR name LIKE ?
                   OR email LIKE ?
                   OR course LIKE ?
                ORDER BY name ASC
                """,
                (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"),
            ).fetchall()
            return [dict(row) for row in rows]

    def count_students(self):
        """Return total number of students."""
        with self._connect() as connection:
            row = connection.execute("SELECT COUNT(*) AS total FROM students").fetchone()
            return row["total"] if row else 0

    def count_courses(self):
        """Return total number of unique courses."""
        with self._connect() as connection:
            row = connection.execute(
                "SELECT COUNT(DISTINCT course) AS total FROM students"
            ).fetchone()
            return row["total"] if row else 0

    def get_recent_students(self, limit=5):
        """Return the most recently added students."""
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT * FROM students ORDER BY id DESC LIMIT ?",
                (limit,),
            ).fetchall()
            return [dict(row) for row in rows]
