from datetime import date
from app.extensions import db

class WishlistRecord(db.Model):
    __tablename__ = "wishlist_records"
    __table_args__ = (db.UniqueConstraint("student_id", "course_id"),)

    record_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey("users.user_id"), nullable=False)
    course_id = db.Column(db.String(20), db.ForeignKey("courses.course_id"), nullable=False)
    added_date = db.Column(db.Date, default=date.today)                             
    approval_status = db.Column(db.String(10), nullable=False, default="DRAFT")     
    course = db.relationship("Course")

    def request_approval(self) -> bool:
        if self.approval_status not in ("DRAFT", "REJECTED"):
            return False
        self.approval_status = "PENDING"
        return True
