# This file creates the Flask web application and connects the frontend pages
# to the business logic. It acts like the main entry point for the website.
import os
import sys

# Add the project root to Python's import path so the app can import the
# project modules correctly when started from the backend folder.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, redirect, render_template, request, url_for

# Import the service layer that contains validation and business rules.
from src.services.student_service import StudentService

# Create the Flask app and point it to the frontend template and static folders.
app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "frontend", "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "frontend", "static"),
)
app.config["SECRET_KEY"] = "student-management-system"

# One shared service instance is used by all routes.
service = StudentService()


@app.route("/")
def index():
    """Redirect the home page to the dashboard page."""
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    """Show dashboard cards and the full student table on the main page."""
    summary = service.get_dashboard_summary()
    return render_template("dashboard.html", summary=summary)


@app.route("/courses")
def courses():
    """Show course-count information and a list of all courses."""
    summary = service.get_dashboard_summary()
    return render_template("courses.html", summary=summary)


@app.route("/reports")
def reports():
    """Display the report page with totals and course data."""
    summary = service.get_dashboard_summary()
    return render_template("reports.html", summary=summary)


@app.route("/settings")
def settings():
    """Display system settings information for the app."""
    summary = service.get_dashboard_summary()
    return render_template("settings.html", summary=summary)


@app.route("/students", methods=["GET", "POST"])
def students():
    """Display all student records and allow adding a new student."""
    if request.method == "POST":
        # Read form values from the browser form and build a dictionary.
        student_data = {
            "student_id": request.form.get("student_id", ""),
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "course": request.form.get("course", ""),
            "year": request.form.get("year", ""),
            "address": request.form.get("address", ""),
        }

        try:
            # Validation happens in the service layer before saving to SQLite.
            service.add_student(student_data)
            return redirect(url_for("students"))
        except ValueError as exc:
            # If validation fails, show a user-friendly message in the page.
            return render_template(
                "students.html",
                students=service.get_all_students(),
                error=str(exc),
            )

    students_list = service.get_all_students()
    return render_template("students.html", students=students_list, error=None)


@app.route("/students/<student_id>")
def student_detail(student_id):
    """Show the details of a student in a dedicated page."""
    student = service.get_student_by_id(student_id)
    return render_template("student_detail.html", student=student)


@app.route("/students/<student_id>/edit", methods=["GET", "POST"])
def edit_student(student_id):
    """Update an existing student record with a form."""
    if request.method == "POST":
        student_data = {
            "student_id": request.form.get("student_id", ""),
            "name": request.form.get("name", ""),
            "email": request.form.get("email", ""),
            "phone": request.form.get("phone", ""),
            "course": request.form.get("course", ""),
            "year": request.form.get("year", ""),
            "address": request.form.get("address", ""),
        }

        try:
            service.update_student(student_id, student_data)
            return redirect(url_for("student_detail", student_id=student_data["student_id"]))
        except ValueError as exc:
            student = service.get_student_by_id(student_id)
            return render_template("student_form.html", student=student, error=str(exc), mode="edit")

    student = service.get_student_by_id(student_id)
    return render_template("student_form.html", student=student, error=None, mode="edit")


@app.route("/students/<student_id>/delete", methods=["POST"])
def delete_student(student_id):
    """Delete a student and return to the student list."""
    try:
        service.delete_student(student_id)
    except ValueError:
        pass
    return redirect(url_for("students"))


@app.route("/students/search")
def search_students():
    """Search students by keyword and show matching results in the same page."""
    keyword = request.args.get("q", "")
    results = service.search_students(keyword)
    return render_template("students.html", students=results, error=None, keyword=keyword)


if __name__ == "__main__":
    # Run the Flask development server locally.
    app.run(debug=True, host="0.0.0.0", port=5000)
