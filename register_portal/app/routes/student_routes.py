from flask import Blueprint, render_template, request, redirect, url_for, current_app

from app import demo_data as db_demo
from app.routes.context import student_ctx
from app.routes.decorators import role_required

student_bp = Blueprint("student", __name__, url_prefix="/student")

COURSES = db_demo.COURSES
GRADES = db_demo.GRADES
STATE = db_demo.STATE


def _selected():
    return [c for c in COURSES if c["status"] == "Selected"]


@student_bp.route("/search")
@role_required("student")
def course_search():
    q = request.args.get("q", "").strip().lower()
    filtered = [
        c for c in COURSES
        if not q or q in c["code"].lower() or q in c["name"].lower()
    ]
    return render_template(
        "student/course_search.html",
        courses=filtered,
        selected_count=len(_selected()),
        active_page="search",
        **student_ctx()
    )


@student_bp.route("/select/<code>", methods=["POST"])
@role_required("student")
def select_course(code):
    for c in COURSES:
        if c["code"] == code and c["status"] == "Available":
            c["status"] = "Selected"
    return redirect(url_for("student.course_search"))


@student_bp.route("/drop/<code>", methods=["POST"])
@role_required("student")
def drop_course(code):
    for c in COURSES:
        if c["code"] == code and c["status"] == "Selected":
            c["status"] = "Available"
    return redirect(url_for("student.course_registration"))


@student_bp.route("/registration")
@role_required("student")
def course_registration():
    selected = _selected()
    total_credits = sum(c["credits"] for c in selected)
    total_tuition = total_credits * current_app.config["TUITION_PER_CREDIT"]
    all_valid = (all(c["prereq_ok"] for c in selected)
                 and total_credits <= current_app.config["MAX_CREDITS"])
    return render_template(
        "student/course_reg.html",
        selected_courses=selected,
        total_credits=total_credits,
        total_tuition=total_tuition,
        all_valid=all_valid,
        confirmed_msg=STATE["confirmed_msg"],
        active_page="registration",
        **student_ctx()
    )


@student_bp.route("/registration/confirm", methods=["POST"])
@role_required("student")
def confirm_registration():
    STATE["confirmed_msg"] = f"Saved {len(_selected())} classes for Semester I · 2026–2027."
    return redirect(url_for("student.course_registration"))


@student_bp.route("/timetable")
@role_required("student")
def student_timetable():
    return render_template(
        "student/timetable.html",
        selected_courses=_selected(),
        active_page="timetable",
        **student_ctx()
    )


@student_bp.route("/results")
@role_required("student")
def student_results():
    return render_template(
        "student/results.html",
        grades=GRADES,
        active_page="results",
        **student_ctx()
    )


@student_bp.route("/tuition")
@role_required("student")
def student_tuition():
    total_credits = sum(c["credits"] for c in _selected())
    tuition_total = total_credits * current_app.config["TUITION_PER_CREDIT"]
    tuition_due = max(0, tuition_total - STATE["tuition_paid"])
    return render_template(
        "student/tuition.html",
        selected_courses=_selected(),
        tuition_total=tuition_total,
        tuition_paid=STATE["tuition_paid"],
        tuition_due=tuition_due,
        active_page="tuition",
        **student_ctx()
    )


@student_bp.route("/tuition/pay", methods=["POST"])
@role_required("student")
def pay_tuition():
    total_credits = sum(c["credits"] for c in _selected())
    STATE["tuition_paid"] = total_credits * current_app.config["TUITION_PER_CREDIT"]
    return redirect(url_for("student.student_tuition"))
