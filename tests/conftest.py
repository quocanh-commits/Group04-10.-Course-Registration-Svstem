import os
from datetime import date, datetime
from types import SimpleNamespace

# Phải đặt TRƯỚC khi import config/app: tránh phụ thuộc vào .env hay PostgreSQL khi test
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")
os.environ.setdefault("SECRET_KEY", "test-secret")

import pytest

from app import create_app
from app.extensions import db
from app.models import Administrator, ClassSection, Course, Lecturer, RegistrationTerm, Student
from app.models.user import hash_password
from app.services.schedule_utils import VN_TZ
from config import Config


class ConfigForTests(Config):
    TESTING = True
    SECRET_KEY = "test-secret"
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"   # DB tạm trong RAM, mỗi test một DB mới
    MAX_CREDITS = 24


@pytest.fixture(scope="session")
def password_hash():
    """bcrypt (12 vòng) khá chậm nên chỉ băm 1 lần cho cả phiên test."""
    return hash_password("123456")


@pytest.fixture()
def app():
    app = create_app(ConfigForTests)
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def data(app, password_hash):
    """Bộ dữ liệu tối thiểu: 1 admin, 1 giảng viên, 1 sinh viên, 1 học kỳ đang OPEN."""
    admin = Administrator(id="A0001", full_name="Admin Test", password_hash=password_hash,
                          email="admin@test.vn", admin_role="Registrar")
    lecturer = Lecturer(id="L0001", full_name="Lecturer Test", password_hash=password_hash,
                        email="lecturer@test.vn", department="CS")
    student = Student(id="S0001", full_name="Student Test", password_hash=password_hash,
                      email="student@test.vn", enrollment_year=2024, major="CS")
    term = RegistrationTerm(id="2026-1", semester_name="Fall 2026",
                            start_date=date(2026, 9, 1), end_date=date(2026, 12, 31),
                            registration_open=date(2026, 8, 1), registration_close=date(2026, 8, 31),
                            status="OPEN", admin_id="A0001")
    db.session.add_all([admin, lecturer, student, term])
    db.session.commit()
    return SimpleNamespace(admin=admin, lecturer=lecturer, student=student, term=term)


@pytest.fixture()
def make_course(data):
    def _make(course_id, title=None, credits=3):
        course = Course(id=course_id, title=title or f"Course {course_id}",
                        credits=credits, admin_id="A0001")
        db.session.add(course)
        db.session.commit()
        return course
    return _make


@pytest.fixture()
def make_class(data):
    def _make(class_id, course, *, hour=8, day=7, capacity=30, enrolled=0):
        cls = ClassSection(id=class_id, course_id=course.id, lecturer_id="L0001",
                           term_id="2026-1", room="R101",
                           schedule_time=datetime(2026, 9, day, hour, 0, tzinfo=VN_TZ),
                           max_capacity=capacity, current_enrollment=enrolled)
        db.session.add(cls)
        db.session.commit()
        return cls
    return _make
