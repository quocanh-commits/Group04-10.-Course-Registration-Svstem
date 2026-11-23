from sqlalchemy import or_

from app.extensions import db
from app.models.class_section import ClassSection
from app.models.course import Course
from app.models.enrollment import Enrollment
from app.models.payment import Payment
from app.models.registration_term import RegistrationTerm
from app.models.user import Student, Lecturer, Administrator
from app.models.wishlist_record import WishlistRecord

MODEL_BY_ROLE = {
    "student": Student,
    "lecturer": Lecturer,
    "admin": Administrator,
}
ID_PREFIX = {"student": "S", "lecturer": "L", "admin": "A"}


def find_by_id(role, user_id):
    """Tra tài khoản theo vai trò (mỗi vai trò một bảng). Trả None nếu không có."""
    model = MODEL_BY_ROLE.get(role)
    if model is None:
        return None
    return db.session.get(model, user_id)


def list_users(role, keyword=""):
    model = MODEL_BY_ROLE[role]
    q = model.query
    if keyword:
        like = f"%{keyword}%"
        q = q.filter(or_(model.id.ilike(like), model.full_name.ilike(like), model.email.ilike(like)))
    return q.order_by(model.id).all()


def count(role):
    return MODEL_BY_ROLE[role].query.count()


def next_id(role):
    model = MODEL_BY_ROLE[role]
    last = db.session.query(db.func.max(model.id)).scalar()
    number = int(last[1:]) + 1 if last else 1
    if number > 9999:
        raise ValueError("Het ma tai khoan")
    return f"{ID_PREFIX[role]}{number:04d}"


def email_exists(role, email, exclude_id=None):
    model = MODEL_BY_ROLE[role]
    q = model.query.filter(db.func.lower(model.email) == email.lower())
    if exclude_id:
        q = q.filter(model.id != exclude_id)
    return q.first() is not None


def dependents(role, user_id):
    """Số bản ghi đang tham chiếu tới tài khoản (chặn xóa nếu > 0)."""
    checks = {
        "student": [("enrollments", Enrollment, Enrollment.student_id),
                    ("wishlist records", WishlistRecord, WishlistRecord.student_id),
                    ("payments", Payment, Payment.student_id)],
        "lecturer": [("class sections", ClassSection, ClassSection.lecturer_id)],
        "admin": [("courses", Course, Course.admin_id),
                  ("registration terms", RegistrationTerm, RegistrationTerm.admin_id)],
    }[role]
    result = {}
    for label, model, column in checks:
        n = model.query.filter(column == user_id).count()
        if n:
            result[label] = n
    return result


def add(user):
    db.session.add(user)


def delete(user):
    db.session.delete(user)
