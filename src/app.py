# This is the console-version entry point.
# It starts the menu-based application for beginners who want to understand the project
# without using the web interface.
from src.controllers.student_controller import StudentController


def main():
    """Start the application."""
    app = StudentController()
    app.run()


if __name__ == "__main__":
    main()
