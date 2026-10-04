import os
import sys

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from flask import Flask, redirect, render_template, request, url_for

from src.services.student_service import StudentService

app = Flask(
    __name__,
    template_folder=os.path.join(PROJECT_ROOT, "frontend", "templates"),
    static_folder=os.path.join(PROJECT_ROOT, "frontend", "static"),
)
app.config["SECRET_KEY"] = "student-management-system"

service = StudentService()


@app.route("/")
def index():
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    summary = service.get_dashboard_summary()
    return render_template("dashboard.html", summary=summary)


@app.route("/students", methods=["GET", "POST"])
def students():
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
            service.add_student(student_data)
            return redirect(url_for("students"))
        except ValueError as exc:
            return render_template("students.html", students=service.get_all_students(), error=str(exc))

    students_list = service.get_all_students()
    return render_template("students.html", students=students_list, error=None)


@app.route("/students/search")
def search_students():
    keyword = request.args.get("q", "")
    results = service.search_students(keyword)
    return render_template("students.html", students=results, error=None, keyword=keyword)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
