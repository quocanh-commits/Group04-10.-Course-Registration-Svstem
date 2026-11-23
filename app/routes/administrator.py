from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.routes.context import admin_ctx
from app.routes.decorators import role_required
from app.services import (account_service, course_admin_service, overview_service,
                          term_service, wishlist_service)
from app.services.errors import ServiceError

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def _run(action, *args):
    """Chạy một hành động của service, hiện thông báo thành công hoặc lỗi nghiệp vụ."""
    try:
        flash(action(*args), "success")
        return True
    except ServiceError as error:
        flash(str(error), "error")
        return False


def _admin_id():
    return session["user_id"]


# ------------------------------------------------------------------ tổng quan
@admin_bp.route("/overview")
@role_required("admin")
def admin_overview():
    return render_template("admin/overview.html", stats=overview_service.get_overview(),
                           active_page="overview", **admin_ctx())


# --------------------------------------- Manage Registration Term (DFD 2.0)
@admin_bp.route("/periods")
@role_required("admin")
def admin_periods():
    edit_id = request.args.get("edit", "")
    values = term_service.form_values(edit_id) if edit_id else None
    return render_template("admin/registration_periods.html", terms=term_service.list_terms(),
                           form=values, active_page="periods", **admin_ctx())


@admin_bp.route("/periods/save", methods=["POST"])
@role_required("admin")
def save_period():
    term_id = request.form.get("term_id", "").strip()
    if term_id:
        _run(term_service.update_term, term_id, request.form)
    else:
        _run(term_service.create_term, _admin_id(), request.form)
    return redirect(url_for("admin.admin_periods"))


@admin_bp.route("/periods/<term_id>/open", methods=["POST"])
@role_required("admin")
def open_period(term_id):
    _run(term_service.open_registration, term_id)
    return redirect(url_for("admin.admin_periods"))


@admin_bp.route("/periods/<term_id>/close", methods=["POST"])
@role_required("admin")
def close_period(term_id):
    _run(term_service.close_registration, term_id)
    return redirect(url_for("admin.admin_periods"))


@admin_bp.route("/periods/<term_id>/delete", methods=["POST"])
@role_required("admin")
def delete_period(term_id):
    _run(term_service.delete_term, term_id)
    return redirect(url_for("admin.admin_periods"))


# ----------------------------------- Manage Curriculum Courses (DFD 2.0)
@admin_bp.route("/curriculum")
@role_required("admin")
def admin_curriculum():
    edit_id = request.args.get("edit", "")
    values = course_admin_service.course_form_values(edit_id) if edit_id else None
    return render_template("admin/curriculum.html", courses=course_admin_service.list_courses(),
                           form=values, active_page="curriculum", **admin_ctx())


@admin_bp.route("/curriculum/save", methods=["POST"])
@role_required("admin")
def save_course():
    course_id = request.form.get("course_id", "").strip()
    if course_id:
        _run(course_admin_service.update_course, course_id, request.form)
    else:
        _run(course_admin_service.create_course, _admin_id(), request.form)
    return redirect(url_for("admin.admin_curriculum"))


@admin_bp.route("/curriculum/<course_id>/delete", methods=["POST"])
@role_required("admin")
def delete_course(course_id):
    _run(course_admin_service.delete_course, course_id)
    return redirect(url_for("admin.admin_curriculum"))


# ------------------------------------------ Class sections / assignments
@admin_bp.route("/assignments")
@role_required("admin")
def admin_assignments():
    terms = term_service.term_options()
    term_id = request.args.get("term", "")
    if term_id not in {t["id"] for t in terms}:
        current = next((t for t in terms if t["status"] == "OPEN"), terms[0] if terms else None)
        term_id = current["id"] if current else ""
    edit_id = request.args.get("edit", "")
    values = course_admin_service.class_form_values(edit_id) if edit_id else None
    return render_template(
        "admin/teaching_assignments.html",
        terms=terms, term_id=term_id,
        classes=course_admin_service.list_classes(term_id) if term_id else [],
        courses=course_admin_service.course_options(),
        lecturers=course_admin_service.lecturer_options(),
        form=values, active_page="assignments", **admin_ctx())


@admin_bp.route("/assignments/save", methods=["POST"])
@role_required("admin")
def save_class():
    class_id = request.form.get("class_id", "").strip()
    if class_id:
        _run(course_admin_service.update_class, class_id, request.form)
    else:
        _run(course_admin_service.create_class, request.form)
    return redirect(url_for("admin.admin_assignments", term=request.form.get("term_id", "")))


@admin_bp.route("/assignments/<class_id>/delete", methods=["POST"])
@role_required("admin")
def delete_class(class_id):
    _run(course_admin_service.delete_class, class_id)
    return redirect(url_for("admin.admin_assignments", term=request.form.get("term_id", "")))


# ------------------------------------------------- Manage Users (DFD 1.0)
@admin_bp.route("/accounts")
@role_required("admin")
def admin_accounts():
    role = request.args.get("role", "student")
    if role not in account_service.ROLES:
        role = "student"
    keyword = request.args.get("q", "").strip()
    edit_id = request.args.get("edit", "")
    values = account_service.form_values(role, edit_id) if edit_id else None
    return render_template(
        "admin/accounts.html",
        role=role, role_labels=account_service.ROLE_LABEL, keyword=keyword,
        accounts=account_service.list_accounts(role, keyword),
        form=values, active_page="accounts", **admin_ctx())


@admin_bp.route("/accounts/save", methods=["POST"])
@role_required("admin")
def save_account():
    role = request.form.get("role", "student")
    user_id = request.form.get("user_id", "").strip()
    try:
        account_service.check_role(role)
    except ServiceError as error:
        flash(str(error), "error")
        return redirect(url_for("admin.admin_accounts"))
    if user_id:
        _run(account_service.update_account, role, user_id, request.form)
    else:
        _run(account_service.create_account, role, request.form)
    return redirect(url_for("admin.admin_accounts", role=role))


@admin_bp.route("/accounts/<role>/<user_id>/reset", methods=["POST"])
@role_required("admin")
def reset_account_password(role, user_id):
    _run(account_service.reset_password, role, user_id)
    return redirect(url_for("admin.admin_accounts", role=role))


@admin_bp.route("/accounts/<role>/<user_id>/delete", methods=["POST"])
@role_required("admin")
def delete_account(role, user_id):
    _run(account_service.delete_account, role, user_id, _admin_id())
    return redirect(url_for("admin.admin_accounts", role=role))


# --------------------------------------------------- Course approval
@admin_bp.route("/wishlist")
@role_required("admin")
def admin_wishlist():
    status = request.args.get("status", "PENDING").upper()
    if status not in wishlist_service.STATUSES and status != "ALL":
        status = "PENDING"
    return render_template(
        "admin/wishlist.html",
        records=wishlist_service.list_records(None if status == "ALL" else status),
        counts=wishlist_service.counts(), status=status,
        active_page="wishlist", **admin_ctx())


@admin_bp.route("/wishlist/<int:record_id>/<decision>", methods=["POST"])
@role_required("admin")
def review_wishlist(record_id, decision):
    _run(wishlist_service.review, record_id, decision.upper())
    return redirect(url_for("admin.admin_wishlist", status=request.form.get("status", "PENDING")))
