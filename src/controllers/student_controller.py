from src.services.student_service import StudentService


class StudentController:
    """Handles user interaction through the terminal menu."""

    def __init__(self, service=None):
        self.service = service or StudentService()

    def _print_student_table(self, students):
        """Display student records in a neat table format."""
        if not students:
            print("No students found.")
            return

        print("\nStudents:")
        print("-" * 120)
        print(f"{'Student ID':<12} {'Name':<20} {'Email':<25} {'Phone':<12} {'Course':<20} {'Year':<6} {'Address':<20}")
        print("-" * 120)
        for student in students:
            print(
                f"{student['student_id']:<12} "
                f"{student['name']:<20} "
                f"{student['email']:<25} "
                f"{student['phone']:<12} "
                f"{student['course']:<20} "
                f"{student['year']:<6} "
                f"{student['address']:<20}"
            )
        print("-" * 120)

    def display_dashboard(self):
        """Show dashboard information with summary counts and all student details."""
        summary = self.service.get_dashboard_summary()
        all_students = summary.get("all_students", [])
        recent_students = summary.get("recent_students", [])

        print("\nDashboard")
        print("=" * 80)
        print(f"Total Students: {summary['total_students']}")
        print(f"Total Courses: {summary['total_courses']}")
        print(f"Active Records: {len(all_students)}")
        print("\nRecently Added Students:")
        if not recent_students:
            print("No students yet.")
        else:
            for student in recent_students:
                print(f"- {student['student_id']} | {student['name']} | {student['course']} | {student['year']}")

        print("\nAll Student Details:")
        if not all_students:
            print("No student records available.")
            return

        self._print_student_table(all_students)

    def add_student(self):
        """Ask the user for student information and add it to the database."""
        print("\nAdd Student")
        student_data = {
            "student_id": input("Student ID: "),
            "name": input("Name: "),
            "email": input("Email: "),
            "phone": input("Phone: "),
            "course": input("Course: "),
            "year": input("Year: "),
            "address": input("Address: "),
        }
        try:
            student_id = self.service.add_student(student_data)
            print(f"Student added successfully with record ID: {student_id}")
        except ValueError as error:
            print(f"Error: {error}")

    def view_students(self):
        """Show all students."""
        students = self.service.get_all_students()
        self._print_student_table(students)

    def view_student_details(self):
        """Show one student by ID."""
        student_id = input("Enter Student ID: ")
        try:
            student = self.service.get_student_by_id(student_id)
            print("\nStudent Details")
            print("=" * 30)
            for key, value in student.items():
                if key != "id":
                    print(f"{key.title()}: {value}")
        except ValueError as error:
            print(f"Error: {error}")

    def update_student(self):
        """Update an existing student record."""
        student_id = input("Enter Student ID to update: ")
        try:
            existing_student = self.service.get_student_by_id(student_id)
            print("Leave blank to keep the current value.")
            updated_data = {
                "student_id": input(f"Student ID [{existing_student['student_id']}]: ") or existing_student["student_id"],
                "name": input(f"Name [{existing_student['name']}]: ") or existing_student["name"],
                "email": input(f"Email [{existing_student['email']}]: ") or existing_student["email"],
                "phone": input(f"Phone [{existing_student['phone']}]: ") or existing_student["phone"],
                "course": input(f"Course [{existing_student['course']}]: ") or existing_student["course"],
                "year": input(f"Year [{existing_student['year']}]: ") or existing_student["year"],
                "address": input(f"Address [{existing_student['address']}]: ") or existing_student["address"],
            }
            self.service.update_student(student_id, updated_data)
            print("Student updated successfully.")
        except ValueError as error:
            print(f"Error: {error}")

    def delete_student(self):
        """Delete a student from the database."""
        student_id = input("Enter Student ID to delete: ")
        try:
            self.service.delete_student(student_id)
            print("Student deleted successfully.")
        except ValueError as error:
            print(f"Error: {error}")

    def search_student(self):
        """Search for students using a keyword."""
        keyword = input("Enter search keyword: ")
        results = self.service.search_students(keyword)
        self._print_student_table(results)

    def show_menu(self):
        """Print the menu for the console application."""
        print("\n=== Student Management System ===")
        print("1. Dashboard")
        print("2. Add Student")
        print("3. View Students")
        print("4. View Student Details")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Search Student")
        print("8. Exit")

    def run(self):
        """Run the main loop for the application."""
        while True:
            try:
                self.show_menu()
                choice = input("Choose an option: ").strip()

                if choice == "1":
                    self.display_dashboard()
                elif choice == "2":
                    self.add_student()
                elif choice == "3":
                    self.view_students()
                elif choice == "4":
                    self.view_student_details()
                elif choice == "5":
                    self.update_student()
                elif choice == "6":
                    self.delete_student()
                elif choice == "7":
                    self.search_student()
                elif choice == "8":
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please choose a number from the menu.")

                try:
                    input("\nPress Enter to continue...")
                except EOFError:
                    print("\nGoodbye!")
                    break
            except EOFError:
                print("\nGoodbye!")
                break
