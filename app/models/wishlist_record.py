from datetime import date

from app.extensions import db


class WishlistRecord(db.Model):
    __tablename__ = "wishlistrecord"
    __table_args__ = (db.UniqueConstraint("studentid", "courseid"),)

    id = db.Column("wishlistid", db.String(5), primary_key=True)
    student_id = db.Column("studentid", db.String(5), db.ForeignKey("student.studentid"), nullable=False)
    course_id = db.Column("courseid", db.String(5), db.ForeignKey("course.courseid"), nullable=False)
    added_date = db.Column("addeddate", db.Date, default=date.today)
    approval_status = db.Column("approvalstatus", db.String(10), nullable=False, default="DRAFT")

    course = db.relationship("Course")

    @property
    def record_id(self):
        return self.id

    @record_id.setter
    def record_id(self, value):
        self.id = value

    def request_approval(self) -> bool:
        if self.approval_status not in ("DRAFT", "REJECTED"):
            return False
        self.approval_status = "PENDING"
        return True