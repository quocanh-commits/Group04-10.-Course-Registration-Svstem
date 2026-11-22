from flask import Blueprint, render_template, request, redirect, url_for, session, flash

from app.services import auth_service

auth_bp = Blueprint("auth", __name__)

ROLE_HOME = {
    "student": "student.course_search",
    "lecturer": "lecturer.lecturer_classes",
    "admin": "admin.admin_overview",
}


@auth_bp.route("/", methods=["GET", "POST"])
def login():
    selected_role = request.form.get("role", "student")
    if request.method == "POST":
        user = auth_service.authenticate(
            request.form.get("username", ""),
            request.form.get("password", ""),
            selected_role,
        )
        if user:
            session.clear()
            session["user_id"] = user.id
            session["username"] = user.id          # S0001 / L0001 / A0001
            session["role"] = user.role
            session["full_name"] = user.full_name
            return redirect(url_for(ROLE_HOME[user.role]))
        flash("Sai tên đăng nhập, mật khẩu hoặc vai trò đã chọn")
    return render_template("sign_in.html", selected_role=selected_role)


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))
