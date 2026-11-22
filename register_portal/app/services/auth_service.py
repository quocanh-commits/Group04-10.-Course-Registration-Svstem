from app.repositories import user_repository


def authenticate(user_id, password, role):
    """Trả về user nếu đúng mã, mật khẩu và vai trò; ngược lại trả None."""
    user = user_repository.find_by_id(role, (user_id or "").strip().upper())
    if user is None or not user.check_password(password or ""):
        return None
    return user
