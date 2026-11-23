from app.extensions import db
from app.models.class_section import ClassSection
from app.models.course import Course


def credit_values():
    rows = db.session.query(Course.credits).distinct().order_by(Course.credits).all()
    return [r[0] for r in rows]


def get(course_id):
    return db.session.get(Course, course_id)


def list_all():
    return Course.query.order_by(Course.id).all()


def count():
    return Course.query.count()


def count_classes(course_id):
    return ClassSection.query.filter(ClassSection.course_id == course_id).count()


def class_counts():
    rows = (db.session.query(ClassSection.course_id, db.func.count(ClassSection.id))
            .group_by(ClassSection.course_id).all())
    return {r[0]: r[1] for r in rows}


def next_id():
    last = db.session.query(db.func.max(Course.id)).scalar()
    number = int(last[1:]) + 1 if last else 1
    return f"C{number:04d}"


def title_exists(title, exclude_id=None):
    q = Course.query.filter(db.func.lower(Course.title) == title.lower())
    if exclude_id:
        q = q.filter(Course.id != exclude_id)
    return q.first() is not None


def add(course):
    db.session.add(course)


def delete(course):
    db.session.delete(course)
