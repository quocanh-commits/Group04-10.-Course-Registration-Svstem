import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.extensions import db
from app.models.user import Student, Lecturer, Administrator, hash_password

DEFAULT_PASSWORD = "123456"
PLACEHOLDER_PREFIX = "$2b$12$abcdefghijklmnopqrstuvwxyz"   # hash giả trong seed.sql

app = create_app()

with app.app_context():
    for model in (Student, Lecturer, Administrator):
        count = 0
        for row in model.query.all():
            if row.password_hash.strip().startswith(PLACEHOLDER_PREFIX):
                row.password_hash = hash_password(DEFAULT_PASSWORD)   # salt riêng cho từng tài khoản
                count += 1
        print(f"{model.__tablename__}: đã sửa {count} tài khoản")
    db.session.commit()