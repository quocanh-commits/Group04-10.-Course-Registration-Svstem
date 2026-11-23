from app.extensions import db
from app.models.class_section import ClassSection
from app.models.enrollment import Enrollment


def find(student_id, class_id):
    return Enrollment.query.filter_by(student_id=student_id, class_id=class_id).first()


def class_ids_of_student(student_id, term_id):
    rows = (db.session.query(Enrollment.class_id)
            .join(ClassSection, ClassSection.id == Enrollment.class_id)
            .filter(Enrollment.student_id == student_id,
                    Enrollment.status == "ENROLLED",
                    ClassSection.term_id == term_id)
            .all())
    return {r[0] for r in rows}


def count_by_term(term_id):
    return (db.session.query(Enrollment.id)
            .join(ClassSection, ClassSection.id == Enrollment.class_id)
            .filter(ClassSection.term_id == term_id).count())


def next_id_number():
    last = db.session.query(db.func.max(Enrollment.id)).scalar()
    return int(last[1:]) + 1 if last else 1


def format_id(number):
    return f"E{number:04d}"


def add(enrollment):
    db.session.add(enrollment)


def delete(enrollment):
    db.session.delete(enrollment)
