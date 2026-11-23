from datetime import datetime

from app.extensions import db


class Enrollment(db.Model):
    __tablename__ = "enrollment"
    __table_args__ = (db.UniqueConstraint("studentid", "classid"),)

    id = db.Column("enrollmentid", db.String(5), primary_key=True)
    student_id = db.Column("studentid", db.String(5), db.ForeignKey("student.studentid"), nullable=False)
    class_id = db.Column("classid", db.String(5), db.ForeignKey("classsection.classid"), nullable=False)
    enrolled_at = db.Column("enrolledat", db.Date, default=datetime.now)
    status = db.Column("status", db.String(100), nullable=False, default="REGISTERED")
    midterm_grade = db.Column("midtermgrade", db.Float)
    final_grade = db.Column("finalgrade", db.Float)

    class_section = db.relationship("ClassSection", back_populates="enrollments")

    @property
    def enrollment_id(self):
        return self.id

    @enrollment_id.setter
    def enrollment_id(self, value):
        self.id = value

    @property
    def midterm(self):
        return self.midterm_grade

    @midterm.setter
    def midterm(self, value):
        self.midterm_grade = value

    @property
    def final(self):
        return self.final_grade

    @final.setter
    def final(self, value):
        self.final_grade = value

    @property
    def created_at(self):
        return self.enrolled_at

    @created_at.setter
    def created_at(self, value):
        self.enrolled_at = value