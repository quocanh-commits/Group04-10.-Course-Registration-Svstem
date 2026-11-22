from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.extensions import db
from app.models.course import Course
from app.models.class_section import ClassSection
from app.models.enrollment import Enrollment
from app.models.wishlist_record import WishlistRecord
from app.models.payment import Payment

student_bp = Blueprint("student", __name__, url_prefix="/student")
# 1. Trang chủ 
@student_bp.route("/")
@login_required
def index():
    return render_template("student/index.html")
# 2. Tìm kiếm học phần
@student_bp.route("/courses")
@login_required
def courses():
    keyword = request.args.get("q", "")

    courses = Course.query.filter(
        Course.course_name.ilike(f"%{keyword}%")
    ).all()

    return render_template(
        "student/registration.html",
        courses=courses
    )
# 3. Đăng ký học phần
@student_bp.route("/register/<int:class_id>")
@login_required
def register(class_id):

    section = ClassSection.query.get_or_404(class_id)

    # Kiểm tra đã đăng ký chưa
    exists = Enrollment.query.filter_by(
        student_id=current_user.id,
        class_section_id=class_id
    ).first()

    if exists:
        flash("Bạn đã đăng ký học phần này!")
        return redirect(url_for("student.courses"))

    enrollment = Enrollment(
        student_id=current_user.id,
        class_section_id=class_id
    )

    db.session.add(enrollment)
    db.session.commit()

    flash("Đăng ký thành công!")

    return redirect(url_for("student.courses"))
# 4. Hủy đăng ký
@student_bp.route("/cancel/<int:class_id>")
@login_required
def cancel(class_id):

    enrollment = Enrollment.query.filter_by(
        student_id=current_user.id,
        class_section_id=class_id
    ).first()

    if enrollment:
        db.session.delete(enrollment)
        db.session.commit()

    flash("Đã hủy đăng ký!")

    return redirect(url_for("student.courses"))
# 5. Danh sách yêu thích
@student_bp.route("/wishlist")
@login_required
def wishlist():

    records = WishlistRecord.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "student/wishlist.html",
        records=records
    )
# Thêm học phần 
@student_bp.route("/wishlist/add/<int:course_id>")
@login_required
def add_wishlist(course_id):

    exists = WishlistRecord.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()

    if not exists:
        record = WishlistRecord(
            student_id=current_user.id,
            course_id=course_id
        )

        db.session.add(record)
        db.session.commit()

    flash("Đã thêm vào yêu thích!")

    return redirect(url_for("student.wishlist"))
# Xóa học phần 
@student_bp.route("/wishlist/delete/<int:course_id>")
@login_required
def delete_wishlist(course_id):

    record = WishlistRecord.query.filter_by(
        student_id=current_user.id,
        course_id=course_id
    ).first()

    if record:
        db.session.delete(record)
        db.session.commit()

    return redirect(url_for("student.wishlist"))
# 6. Thời khóa biểu
@student_bp.route("/timetable")
@login_required
def timetable():

    enrollments = Enrollment.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "student/academic.html",
        enrollments=enrollments,
        mode="timetable"
    )
# 7. Kết quả học tập
@student_bp.route("/results")
@login_required
def results():

    enrollments = Enrollment.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "student/academic.html",
        enrollments=enrollments,
        mode="results"
    )
# 8. Học phí
@student_bp.route("/tuition")
@login_required
def tuition():

    payments = Payment.query.filter_by(
        student_id=current_user.id
    ).all()

    return render_template(
        "student/academic.html",
        payments=payments,
        mode="tuition"
    )
