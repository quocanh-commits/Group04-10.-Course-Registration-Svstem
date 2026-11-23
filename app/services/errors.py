from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db


class ServiceError(Exception):
    """Lỗi nghiệp vụ: nội dung hiển thị thẳng cho người dùng."""


def commit():
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Database error")
        raise ServiceError("Database error. Nothing was saved.")


def parse_date(value, label):
    from datetime import date
    try:
        return date.fromisoformat((value or "").strip())
    except ValueError:
        raise ServiceError(f"{label} is not a valid date")


def parse_int(value, label, low, high):
    try:
        number = int((value or "").strip())
    except ValueError:
        raise ServiceError(f"{label} must be a whole number")
    if not low <= number <= high:
        raise ServiceError(f"{label} must be between {low} and {high}")
    return number
