from app.extensions import db


class Course(db.Model):
    __tablename__ = "course"

    id = db.Column("courseid", db.String(5), primary_key=True)
    title = db.Column("title", db.String(100), nullable=False)
    credits = db.Column("credits", db.Integer, nullable=False)
    admin_id = db.Column("adminid", db.String(5), db.ForeignKey("administrator.adminid"), nullable=False)

    def get_details(self):
        return {"course_id": self.id, "title": self.title, "credits": self.credits}
