from flask import (Blueprint, render_template, request, redirect, url_for,
                   session, flash, current_app)

from app import demo_data
from app.routes.context import student_ctx
from app.routes.decorators import role_required
from app.services import registration_service, search_service

student_bp = Blueprint("student", __name__, url_prefix="/student")

GRADES = demo_data.GRADES     # tạm thời, thay ở bước giảng viên/điểm
STATE = demo_data.STATE       # tạm thời, thay ở bước thanh toán


def _cart():
    return list(session.get("cart", []))


def _save_cart(cart):
    session["cart"] = cart


def _student_id():
    return session["user_id"]


# ---------------------------------------------------------------- tìm môn
@student_bp.route("/search")
@role_required("student")
def course_search():
    keyword = request.args.get("q", "").strip()
    credits = request.args.get("credits", type=int)
    status = request.args.get("status", "")
    cart = _cart()
    term = search_service.current_term_info()
    rows = search_service.search_classes(_student_id(), cart, keyword, credits, status)
    return render_template(
        "student/course_search.html",
        courses=rows,
        term=term,
        registration_open=bool(term and term["open"]),
        credit_options=search_service.credit_options(),
        selected_credits=credits,
        selected_status=status,
        selected_count=len(cart),
        max_credits=current_app.config["MAX_CREDITS"],
        active_page="search",
        **student_ctx()
    )


# ----------------------------------------------- chọn / bỏ chọn (chỉ tạm)
@student_bp.route("/select/<class_id>", methods=["POST"])
@role_required("student")
def select_course(class_id):
    cart = _cart()
    ok, message = registration_service.can_select(_student_id(), class_id, cart)
    if ok:
        cart.append(class_id)
        _save_cart(cart)
    flash(message, "success" if ok else "error")
    return redirect(url_for("student.course_search"))


@student_bp.route("/drop/<class_id>", methods=["POST"])
@role_required("student")
def drop_course(class_id):
    _save_cart([c for c in _cart() if c != class_id])
    return redirect(url_for("student.course_registration"))


# --------------------------------------------------------- đăng ký (ghi DB)
@student_bp.route("/registration")
@role_required("student")
def course_registration():
    plan = registration_service.build_plan(_student_id(), _cart())
    _save_cart(plan["cart_ids"])
    per_credit = current_app.config["TUITION_PER_CREDIT"]
    return render_template(
        "student/course_reg.html",
        term=plan["term"],
        registered_rows=plan["registered_rows"],
        cart_rows=plan["cart_rows"],
        global_problems=plan["global_problems"],
        all_valid=plan["all_valid"],
        total_credits=plan["total_credits"],
        total_tuition=plan["total_credits"] * per_credit,
        max_credits=current_app.config["MAX_CREDITS"],
        tuition_per_credit=per_credit,
        active_page="registration",
        **student_ctx()
    )


@student_bp.route("/registration/confirm", methods=["POST"])
@role_required("student")
def confirm_registration():
    result = registration_service.confirm(_student_id(), _cart())
    if result["ok"]:
        _save_cart([])
        flash(f"Registered {result['count']} class(es) successfully.", "success")
    else:
        for message in result["messages"]:
            flash(message, "error")
    return redirect(url_for("student.course_registration"))


@student_bp.route("/cancel/<class_id>", methods=["POST"])
@role_required("student")
def cancel_registration(class_id):
    ok, message = registration_service.cancel(_student_id(), class_id)
    flash(message, "success" if ok else "error")
    return redirect(url_for("student.course_registration"))


# -------------------------------------------------------- thời khóa biểu
@student_bp.route("/timetable")
@role_required("student")
def student_timetable():
    return render_template(
        "student/timetable.html",
        term=search_service.current_term_info(),
        classes=search_service.view_schedule(_student_id()),
        active_page="timetable",
        **student_ctx()
    )


# ------------------------------------- kết quả, học phí (còn dữ liệu giả)
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
    classes = search_service.view_schedule(_student_id())
    per_credit = current_app.config["TUITION_PER_CREDIT"]
    tuition_total = sum(c["credits"] for c in classes) * per_credit
    tuition_due = max(0, tuition_total - STATE["tuition_paid"])
    return render_template(
        "student/tuition.html",
        selected_courses=classes,
        tuition_per_credit=per_credit,
        tuition_total=tuition_total,
        tuition_paid=STATE["tuition_paid"],
        tuition_due=tuition_due,
        active_page="tuition",
        **student_ctx()
    )


@student_bp.route("/tuition/pay", methods=["POST"])
@role_required("student")
def pay_tuition():
    classes = search_service.view_schedule(_student_id())
    STATE["tuition_paid"] = (sum(c["credits"] for c in classes)
                             * current_app.config["TUITION_PER_CREDIT"])
    return redirect(url_for("student.student_tuition"))
