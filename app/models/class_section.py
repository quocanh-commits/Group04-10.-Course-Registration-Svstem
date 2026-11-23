from app.extensions import db


class ClassSection(db.Model):
    __tablename__ = "classsection"

    id = db.Column("classid", db.String(5), primary_key=True)
    current_enrollment = db.Column("currentenrollment", db.Integer, nullable=False, default=0)
    schedule_time = db.Column("scheduletime", db.DateTime(timezone=True), nullable=False)
    room = db.Column("room", db.String(4), nullable=False)
    max_capacity = db.Column("maxcapacity", db.Integer, nullable=False)
    term_id = db.Column("termid", db.String(10), db.ForeignKey("registrationterm.termid"), nullable=False)
    course_id = db.Column("courseid", db.String(5), db.ForeignKey("course.courseid"), nullable=False)
    lecturer_id = db.Column("lecturerid", db.String(5), db.ForeignKey("lecturer.lecturerid"), nullable=False)

    course = db.relationship("Course")
    term = db.relationship("RegistrationTerm")
    lecturer = db.relationship("Lecturer")
    enrollments = db.relationship("Enrollment", back_populates="class_section")

    def get_available_seats(self):
        return max(0, self.max_capacity - self.current_enrollment)

    def get_enrollments(self):
        return list(self.enrollments)
