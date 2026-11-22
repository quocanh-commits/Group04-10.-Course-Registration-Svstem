from flask import session


def _initials(name):
    return "".join(p[0] for p in name.split()[-2:]).upper()


def student_ctx(**kwargs):
    name = session.get("full_name", "")
    base = {
        "workspace_role": "Student",
        "user_initials": _initials(name),
        "user_name": name,
        "user_sub": f"Student · {session.get('username', '')}",
    }
    base.update(kwargs)
    return base


def lecturer_ctx(**kwargs):
    name = session.get("full_name", "")
    base = {
        "workspace_role": "Lecturer",
        "user_initials": _initials(name),
        "user_name": name,
        "user_sub": "Lecturer · Faculty of IT",
    }
    base.update(kwargs)
    return base


def admin_ctx(**kwargs):
    name = session.get("full_name", "")
    base = {
        "workspace_role": "Administrator",
        "user_initials": _initials(name),
        "user_name": name,
        "user_sub": "Administrator · Academic Affairs",
    }
    base.update(kwargs)
    return base
