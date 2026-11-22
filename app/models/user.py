import bcrypt

from app.extensions import db


def hash_password(raw):
    return bcrypt.hashpw(raw.encode(), bcrypt.gensalt(12)).decode()


def verify_password(raw, hashed):
    try:
        return bcrypt.checkpw(raw.encode(), hashed.strip().encode())
    except ValueError:  # hash không hợp lệ
        return False


class User(db.Model):
    """Lớp trừu tượng User trong UML. Không có bảng riêng; 3 lớp con có bảng riêng."""
    __abstract__ = True
    role = None

    full_name = db.Column("fullname", db.String(50), nullable=False)
    password_hash = db.Column("passwordhash", db.String(60), nullable=False)
    date_of_birth = db.Column("dateofbirth", db.Date)
    email = db.Column("email", db.String(100))

    def check_password(self, raw):
        return verify_password(raw, self.password_hash)


class Student(User):
    __tablename__ = "student"
    role = "student"

    id = db.Column("studentid", db.String(5), primary_key=True)
    enrollment_year = db.Column("enrollmentyear", db.Integer)
    major = db.Column("major", db.String(100))


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
