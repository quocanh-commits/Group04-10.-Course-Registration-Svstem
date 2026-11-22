from flask import Blueprint, render_template

from app import demo_data
from app.routes.context import admin_ctx
from app.routes.decorators import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/overview")
@role_required("admin")
def admin_overview():
    return render_template("admin/overview.html", active_page="overview", **admin_ctx())


@admin_bp.route("/periods")
@role_required("admin")
def admin_periods():
    return render_template("admin/registration_periods.html", periods=demo_data.PERIODS,
                           active_page="periods", **admin_ctx())


@admin_bp.route("/curriculum")
@role_required("admin")
def admin_curriculum():
    return render_template("admin/curriculum.html", courses=demo_data.COURSES,
                           active_page="curriculum", **admin_ctx())


@admin_bp.route("/assignments")
@role_required("admin")
def admin_assignments():
    return render_template("admin/teaching_assignments.html", classes=demo_data.COURSES,
                           active_page="assignments", **admin_ctx())


@admin_bp.route("/accounts")
@role_required("admin")
def admin_accounts():
    return render_template("admin/accounts.html", accounts=demo_data.ACCOUNTS,
                           active_page="accounts", **admin_ctx())
