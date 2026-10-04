from src.controllers.student_controller import StudentController


def main():
    """Start the application."""
    app = StudentController()
    app.run()


if __name__ == "__main__":
    main()
