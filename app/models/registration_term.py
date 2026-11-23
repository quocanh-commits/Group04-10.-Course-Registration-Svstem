from app.extensions import db


class RegistrationTerm(db.Model):
    __tablename__ = "registrationterm"

    id = db.Column("termid", db.String(10), primary_key=True)
    semester_name = db.Column("semestername", db.String(10), nullable=False)
    start_date = db.Column("startdate", db.Date, nullable=False)
    end_date = db.Column("enddate", db.Date, nullable=False)
    registration_open = db.Column("registrationopen", db.Date, nullable=False)
    registration_close = db.Column("registrationclose", db.Date, nullable=False)
    status = db.Column("status", db.String(10), nullable=False)
    admin_id = db.Column("adminid", db.String(5), db.ForeignKey("administrator.adminid"), nullable=False)

    @property
    def name(self):
        return (self.semester_name or "").strip()

    def is_registration_open(self):
        """Dựa vào cột status (OPEN), không so sánh ngày."""
        return (self.status or "").strip().upper() == "OPEN"
