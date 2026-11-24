import pytest

from app.models.user import hash_password, verify_password
from app.services import auth_service


# ------------------------------------------------------------------ bcrypt
def test_hash_is_real_bcrypt_and_verifies():
    hashed = hash_password("123456")
    assert hashed.startswith("$2b$12$") and len(hashed) == 60
    assert verify_password("123456", hashed)
    assert not verify_password("sai-mat-khau", hashed)


def test_same_password_gets_different_salt():
    assert hash_password("123456") != hash_password("123456")


def test_placeholder_hash_is_rejected_without_crashing():
    """Hash giả trong seed.sql phải bị từ chối (False), không được làm app lỗi."""
    fake = "$2b$12$abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQ"
    assert verify_password("123456", fake) is False


# ------------------------------------------------------------- auth_service
@pytest.mark.parametrize("role,uid", [("student", "S0001"), ("lecturer", "L0001"), ("admin", "A0001")])
def test_authenticate_success(data, role, uid):
    user = auth_service.authenticate(uid, "123456", role)
    assert user is not None and user.id == uid and user.role == role


def test_authenticate_normalizes_id(data):
    assert auth_service.authenticate("  s0001 ", "123456", "student") is not None


def test_authenticate_wrong_password(data):
    assert auth_service.authenticate("S0001", "654321", "student") is None


def test_authenticate_wrong_role(data):
    assert auth_service.authenticate("S0001", "123456", "lecturer") is None


def test_authenticate_unknown_user_or_role(data):
    assert auth_service.authenticate("S9999", "123456", "student") is None
    assert auth_service.authenticate("S0001", "123456", "hacker") is None


def test_authenticate_empty_values(data):
    assert auth_service.authenticate("", "", "student") is None
    assert auth_service.authenticate(None, None, "student") is None


# ------------------------------------------------------------------- route
def test_login_page_loads(client):
    assert client.get("/").status_code == 200


@pytest.mark.parametrize("role,uid", [("student", "S0001"), ("lecturer", "L0001"), ("admin", "A0001")])
def test_login_success_redirects_and_sets_session(client, data, role, uid):
    resp = client.post("/", data={"role": role, "username": uid, "password": "123456"})
    assert resp.status_code == 302
    with client.session_transaction() as sess:
        assert sess["user_id"] == uid
        assert sess["role"] == role


def test_login_wrong_password_stays_on_page(client, data):
    resp = client.post("/", data={"role": "student", "username": "S0001", "password": "sai"})
    assert resp.status_code == 200
    with client.session_transaction() as sess:
        assert "user_id" not in sess


def test_logout_clears_session(client, data):
    client.post("/", data={"role": "student", "username": "S0001", "password": "123456"})
    assert client.get("/logout").status_code == 302
    with client.session_transaction() as sess:
        assert "user_id" not in sess
