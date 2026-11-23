from app.extensions import db

class ClassSection(db.Model):
    __tablename__ = "class_sections"

    class_id = db.Column(db.String(30), primary_key=True)
    course_id = db.Column(db.String(20), db.ForeignKey("courses.course_id"), nullable=False)
    term_id = db.Column(db.Integer, db.ForeignKey("registration_terms.term_id"), nullable=False)
    lecturer_id = db.Column(db.String(20), db.ForeignKey("users.user_id"))
    room = db.Column(db.String(30))
    day_of_week = db.Column(db.Integer, nullable=False)       # 2..8
    start_period = db.Column(db.Integer, nullable=False)
    end_period = db.Column(db.Integer, nullable=False)
    capacity = db.Column(db.Integer, nullable=False, default=50)

    course = db.relationship("Course")
    term = db.relationship("RegistrationTerm")
    lecturer = db.relationship("User", foreign_keys=[lecturer_id])

    def conflicts_with(self, other: "ClassSection") -> bool:
        return (self.term_id == other.term_id and self.day_of_week == other.day_of_week
                and self.start_period <= other.end_period
                and other.start_period <= self.end_period)
