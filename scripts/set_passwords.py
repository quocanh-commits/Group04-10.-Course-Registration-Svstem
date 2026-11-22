"""Ghi đè hash giả trong seed.sql bằng hash bcrypt thật của mật khẩu mặc định.

Chạy từ thư mục gốc dự án:  python scripts/set_passwords.py
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import Student, Lecturer, Administrator, hash_password

DEFAULT_PASSWORD = "123456"

app = create_app()

with app.app_context():
    new_hash = hash_password(DEFAULT_PASSWORD)
    for model in (Student, Lecturer, Administrator):
        rows = model.query.all()
        for row in rows:
            row.password_hash = new_hash
        print(f"{model.__tablename__}: {len(rows)} tài khoản") 
    db.session.commit()
    print("Xong. Mật khẩu mặc định:", DEFAULT_PASSWORD)
