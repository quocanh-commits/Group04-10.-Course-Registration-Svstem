import secrets

import bcrypt
from flask import session

from app.extensions import db


def hash_password(raw: str) -> str:
    return bcrypt.hashpw(raw.encode(), bcrypt.gensalt(12)).decode()


def verify_password(raw: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(raw.encode(), hashed.strip().encode())
    except ValueError:
        return False


class User(db.Model):
    """Lớp trừu tượng User. Các phương thức do lớp con cài đặt hoặc dùng chung."""
    __abstract__ = True
    role = None

    full_name = db.Column("fullname", db.String(50), nullable=False)
    password_hash = db.Column("passwordhash", db.String(60), nullable=False)
    date_of_birth = db.Column("dateofbirth", db.Date)
    email = db.Column("email", db.String(100))

    @property
    def user_id(self):
        return self.id

    @user_id.setter
    def user_id(self, value):
        self.id = value

    def set_password(self, raw: str) -> None:
        self.password_hash = hash_password(raw)

    def check_password(self, raw: str) -> bool:
        return verify_password(raw, self.password_hash)

    def login(self, user_id: str, password: str) -> bool:
        return self.id == user_id and self.check_password(password)

    def logout(self) -> None:
        session.clear()

    def reset_password(self, email: str) -> bool:
        if email != self.email:
            return False
        self.set_password(secrets.token_urlsafe(8))
        return True

    def search_course(self, keyword: str = ""):
        from app.services import search_service
        return search_service.search_courses(keyword)

    def classes_info(self, class_id: str):
        from app.services import class_service
        return class_service.get_class(class_id)

    def view_schedule(self):
        from app.services import class_service
        return class_service.get_timetable(self.id)[1]


class Student(User):
    __tablename__ = "student"
    role = "student"

    id = db.Column("studentid", db.String(5), primary_key=True)
    enrollment_year = db.Column("enrollmentyear", db.Integer)
    major = db.Column("major", db.String(100))

    def add_to_wishlist(self, course_id: str) -> bool:
        from app.services import wishlist_service
        return wishlist_service.add_to_wishlist(self.id, course_id).ok

    def register_class(self, class_id: str):
        from app.services import registration_service
        return registration_service.register_class(self.id, class_id)

    def make_payment(self, amount: int | None = None, payment_id: str | None = None):
        from app.services import payment_service
        return payment_service.make_payment(self.id)


class Lecturer(User):
    __tablename__ = "lecturer"
    role = "lecturer"

    id = db.Column("lecturerid", db.String(5), primary_key=True)
    department = db.Column("department", db.String(100))


class Administrator(User):
    __tablename__ = "administrator"
    role = "admin"

    id = db.Column("adminid", db.String(5), primary_key=True)
    admin_role = db.Column("adminrole", db.String(100))