from app.extensions import db


class WishlistRecord(db.Model):
    """Cần chạy migration 001 (đổi whistListId thành wishlistId) trước khi dùng."""
    __tablename__ = "wishlistrecord"

    id = db.Column("wishlistid", db.Integer, primary_key=True)
    added_date = db.Column("addeddate", db.Date, nullable=False)
    approval_status = db.Column("approvalstatus", db.String(100), nullable=False)
    student_id = db.Column("studentid", db.String(5), db.ForeignKey("student.studentid"), nullable=False)
    course_id = db.Column("courseid", db.String(5), db.ForeignKey("course.courseid"), nullable=False)

    student = db.relationship("Student")
    course = db.relationship("Course")
