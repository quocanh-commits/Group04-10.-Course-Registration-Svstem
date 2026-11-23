from sqlalchemy import func, or_
from sqlalchemy.orm import contains_eager, joinedload

from app.extensions import db
from app.models.class_section import ClassSection
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.user import Lecturer


def search(term_id, keyword="", credits=None):
    q = (ClassSection.query
         .join(ClassSection.course)
         .join(ClassSection.lecturer)
         .options(contains_eager(ClassSection.course), contains_eager(ClassSection.lecturer))
         .filter(ClassSection.term_id == term_id))
    if keyword:
        like = f"%{keyword}%"
        q = q.filter(or_(Course.title.ilike(like), Course.id.ilike(like),
                         ClassSection.id.ilike(like), Lecturer.full_name.ilike(like)))
    if credits:
        q = q.filter(Course.credits == credits)
    return q.order_by(Course.id, ClassSection.id).all()


def get(class_id, lock=False):
    q = ClassSection.query.filter(ClassSection.id == class_id)
    if lock:
        q = q.with_for_update()
    return q.first()


def get_many(class_ids, lock=False):
    """Trả các lớp theo đúng thứ tự class_ids, bỏ qua mã không tồn tại."""
    if not class_ids:
        return []
    q = ClassSection.query.filter(ClassSection.id.in_(class_ids))
    if lock:
        q = q.with_for_update()
    found = {c.id: c for c in q.all()}
    return [found[i] for i in class_ids if i in found]


def find_registered(student_id, term_id):
    return (ClassSection.query
            .join(Enrollment, Enrollment.class_id == ClassSection.id)
            .options(joinedload(ClassSection.course), joinedload(ClassSection.lecturer))
            .filter(Enrollment.student_id == student_id,
                    Enrollment.status == "ENROLLED",
                    ClassSection.term_id == term_id)
            .order_by(ClassSection.id)
            .all())


# ------------------------------------------------------------- dành cho admin
def list_by_term(term_id):
    return (ClassSection.query
            .options(joinedload(ClassSection.course), joinedload(ClassSection.lecturer))
            .filter(ClassSection.term_id == term_id)
            .order_by(ClassSection.id)
            .all())


def count_by_term(term_id):
    return ClassSection.query.filter(ClassSection.term_id == term_id).count()


def by_lecturer_in_term(term_id, lecturer_id):
    return ClassSection.query.filter(ClassSection.term_id == term_id,
                                     ClassSection.lecturer_id == lecturer_id).all()


def by_room_in_term(term_id, room):
    return ClassSection.query.filter(ClassSection.term_id == term_id,
                                     func.trim(ClassSection.room) == room).all()


def enrollment_count(class_id):
    return Enrollment.query.filter(Enrollment.class_id == class_id).count()


def next_id():
    last = db.session.query(func.max(ClassSection.id)).scalar()
    number = int(last[2:]) + 1 if last else 1
    return f"CL{number:03d}", number


def add(cls):
    db.session.add(cls)


def delete(cls):
    db.session.delete(cls)
