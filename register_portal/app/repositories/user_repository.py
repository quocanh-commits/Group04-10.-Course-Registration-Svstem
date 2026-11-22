from app.extensions import db
from app.models.user import Student, Lecturer, Administrator

MODEL_BY_ROLE = {
    "student": Student,
    "lecturer": Lecturer,
    "admin": Administrator,
}


def find_by_id(role, user_id):
    """Tra tài khoản theo vai trò (mỗi vai trò một bảng). Trả None nếu không có."""
    model = MODEL_BY_ROLE.get(role)
    if model is None:
        return None
    return db.session.get(model, user_id)


def list_all(model):
    return model.query.all()
