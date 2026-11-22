from flask import Blueprint, render_template, request

from app import demo_data
from app.routes.context import lecturer_ctx
from app.routes.decorators import role_required

lecturer_bp = Blueprint("lecturer", __name__, url_prefix="/lecturer")

COURSES = demo_data.COURSES
ROSTER = demo_data.ROSTER
ANNOUNCEMENTS = demo_data.ANNOUNCEMENTS


@lecturer_bp.route("/classes")
@role_required("lecturer")
def lecturer_classes():
    return render_template(
        "lecturer/teaching_classes.html",
        classes=COURSES,
        active_page="classes",
        **lecturer_ctx()
    )


@lecturer_bp.route("/attendance", methods=["GET", "POST"])
@role_required("lecturer")
def lecturer_attendance():
    if request.method == "POST":
        for st in ROSTER:
            val = request.form.get(f"status_{st['sid']}")
            if val:
                st["status"] = val
    return render_template(
        "lecturer/attendance.html",
        roster=ROSTER,
        active_page="attendance",
        **lecturer_ctx()
    )


@lecturer_bp.route("/grades", methods=["GET", "POST"])
@role_required("lecturer")
def lecturer_grades():
    if request.method == "POST":
        for st in ROSTER:
            try:
                st["midterm"] = float(request.form.get(f"mid_{st['sid']}", st["midterm"]))
                st["final"] = float(request.form.get(f"fin_{st['sid']}", st["final"]))
            except ValueError:
                pass
    return render_template(
        "lecturer/grade_entry.html",
        roster=ROSTER,
        active_page="grades",
        **lecturer_ctx()
    )


@lecturer_bp.route("/announcements", methods=["GET", "POST"])
@role_required("lecturer")
def lecturer_announcements():
    if request.method == "POST":
        ANNOUNCEMENTS.insert(0, {
            "class_code": request.form.get("class_code", "CS205.01").split(" · ")[0],
            "title": request.form.get("title", ""),
            "date": "21/11/2026",
            "body": request.form.get("body", ""),
        })
    return render_template(
        "lecturer/announcements.html",
        announcements=ANNOUNCEMENTS,
        active_page="announcements",
        **lecturer_ctx()
    )
