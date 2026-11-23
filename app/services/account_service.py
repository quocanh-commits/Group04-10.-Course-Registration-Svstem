from datetime import date

from flask import current_app

from app.extensions import db
from app.models.user import Student, Lecturer, Administrator, hash_password
from app.repositories import user_repository
from app.services.errors import ServiceError, commit, parse_date, parse_int

ROLES = ("student", "lecturer", "admin")
ROLE_LABEL = {"student": "Student", "lecturer": "Lecturer", "admin": "Administrator"}
MODEL = {"student": Student, "lecturer": Lecturer, "admin": Administrator}


def check_role(role):
    if role not in ROLES:
        raise ServiceError("Unknown account type")
    return role


def _detail(user):
    if user.role == "student":
        return f"{user.major} · Intake {user.enrollment_year}"
    if user.role == "lecturer":
        return user.department
    return user.admin_role


def list_accounts(role, keyword=""):
    check_role(role)
    return [{
        "id": u.id,
        "name": u.full_name,
        "email": u.email,
        "dob": u.date_of_birth.strftime("%d/%m/%Y") if u.date_of_birth else "",
        "detail": _detail(u),
    } for u in user_repository.list_users(role, keyword)]


def form_values(role, user_id):
    """Giá trị điền sẵn vào form khi sửa. None nếu không có tài khoản."""
    user = user_repository.find_by_id(role, user_id)
    if user is None:
        return None
    values = {
        "user_id": user.id,
        "full_name": user.full_name,
        "email": user.email,
        "date_of_birth": user.date_of_birth.isoformat() if user.date_of_birth else "",
    }
    if role == "student":
        values.update(major=user.major, enrollment_year=user.enrollment_year)
    elif role == "lecturer":
        values.update(department=user.department)
    else:
        values.update(admin_role=user.admin_role)
    return values


def _clean(role, form, exclude_id=None):
    name = (form.get("full_name") or "").strip()
    email = (form.get("email") or "").strip()
    if not name or len(name) > 50:
        raise ServiceError("Full name is required (max 50 characters)")
    if "@" not in email or "." not in email.split("@")[-1] or len(email) > 100:
        raise ServiceError("Email is not valid")
    if user_repository.email_exists(role, email, exclude_id):
        raise ServiceError("This email is already used by another account of the same type")

    dob = parse_date(form.get("date_of_birth"), "Date of birth")
    if dob >= date.today() or dob.year < 1920:
        raise ServiceError("Date of birth is not realistic")

    data = {"full_name": name, "email": email, "date_of_birth": dob}
    if role == "student":
        major = (form.get("major") or "").strip()
        if not major or len(major) > 100:
            raise ServiceError("Major is required (max 100 characters)")
        data["major"] = major
        data["enrollment_year"] = parse_int(form.get("enrollment_year"), "Enrollment year",
                                            2000, date.today().year + 1)
    elif role == "lecturer":
        department = (form.get("department") or "").strip()
        if not department or len(department) > 100:
            raise ServiceError("Department is required (max 100 characters)")
        data["department"] = department
    else:
        admin_role = (form.get("admin_role") or "").strip()
        if not admin_role or len(admin_role) > 100:
            raise ServiceError("Administrator role is required (max 100 characters)")
        data["admin_role"] = admin_role
    return data


def create_account(role, form):
    check_role(role)
    data = _clean(role, form)
    user = MODEL[role](id=user_repository.next_id(role), **data)
    user.password_hash = hash_password(current_app.config["DEFAULT_PASSWORD"])
    user_repository.add(user)
    commit()
    return (f"Created {ROLE_LABEL[role].lower()} account {user.id}. "
            f"Initial password: {current_app.config['DEFAULT_PASSWORD']}")


def update_account(role, user_id, form):
    check_role(role)
    user = user_repository.find_by_id(role, user_id)
    if user is None:
        raise ServiceError("Account not found")
    for field, value in _clean(role, form, exclude_id=user_id).items():
        setattr(user, field, value)
    commit()
    return f"Updated account {user.id}"


def reset_password(role, user_id):
    check_role(role)
    user = user_repository.find_by_id(role, user_id)
    if user is None:
        raise ServiceError("Account not found")
    user.password_hash = hash_password(current_app.config["DEFAULT_PASSWORD"])
    commit()
    return f"Password of {user.id} was reset to {current_app.config['DEFAULT_PASSWORD']}"


def delete_account(role, user_id, current_user_id):
    check_role(role)
    user = user_repository.find_by_id(role, user_id)
    if user is None:
        raise ServiceError("Account not found")
    if role == "admin":
        if user_id == current_user_id:
            raise ServiceError("You cannot delete your own account")
        if user_repository.count("admin") <= 1:
            raise ServiceError("The last administrator account cannot be deleted")
    deps = user_repository.dependents(role, user_id)
    if deps:
        parts = ", ".join(f"{n} {label}" for label, n in deps.items())
        raise ServiceError(f"Cannot delete {user_id}: still referenced by {parts}")
    user_repository.delete(user)
    commit()
    return f"Deleted account {user_id}"
