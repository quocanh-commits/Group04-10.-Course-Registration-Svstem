from datetime import datetime

from app.extensions import db

class Enrollment(db.Model):
    __tablename__ = "enrollments"
    __table_args__ = (db.UniqueConstraint("student_id", "class_id"),)

    enrollment_id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), db.ForeignKey("users.user_id"), nullable=False)
    class_id = db.Column(db.String(30), db.ForeignKey("class_sections.class_id"), nullable=False)
    status = db.Column(db.String(15), nullable=False, default="REGISTERED")  # REGISTERED | CANCELLED
    midterm = db.Column(db.Float)
    final = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.now)

    class_section = db.relationship("ClassSection", backref="enrollments")
