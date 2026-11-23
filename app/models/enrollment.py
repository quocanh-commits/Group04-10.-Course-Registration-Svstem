from app.extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollment"

    id = db.Column("enrollmentid", db.String(5), primary_key=True)
    enrolled_at = db.Column("enrolledat", db.Date, nullable=False)
    status = db.Column("status", db.String(100), nullable=False)
    mid_term_grade = db.Column("midtermgrade", db.Float)   # NULL cho tới khi giảng viên nhập
    final_grade = db.Column("finalgrade", db.Float)
    class_id = db.Column("classid", db.String(5), db.ForeignKey("classsection.classid"), nullable=False)
    student_id = db.Column("studentid", db.String(5), db.ForeignKey("student.studentid"), nullable=False)

    class_section = db.relationship("ClassSection", back_populates="enrollments")
    student = db.relationship("Student")
