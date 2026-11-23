from sqlalchemy import func

from app.extensions import db
from app.models.class_section import ClassSection
from app.models.registration_term import RegistrationTerm


def get_current_term():
    """Học kỳ đang OPEN; nếu không có thì học kỳ có ngày bắt đầu muộn nhất."""
    open_term = (RegistrationTerm.query
                 .filter(func.upper(func.trim(RegistrationTerm.status)) == "OPEN")
                 .order_by(RegistrationTerm.start_date.desc())
                 .first())
    if open_term:
        return open_term
    return RegistrationTerm.query.order_by(RegistrationTerm.start_date.desc()).first()


def get(term_id):
    return db.session.get(RegistrationTerm, term_id)


def list_all():
    return RegistrationTerm.query.order_by(RegistrationTerm.start_date.desc()).all()


def open_terms():
    return (RegistrationTerm.query
            .filter(func.upper(func.trim(RegistrationTerm.status)) == "OPEN").all())


def class_counts():
    rows = (db.session.query(ClassSection.term_id, func.count(ClassSection.id))
            .group_by(ClassSection.term_id).all())
    return {r[0]: r[1] for r in rows}


def add(term):
    db.session.add(term)


def delete(term):
    db.session.delete(term)
