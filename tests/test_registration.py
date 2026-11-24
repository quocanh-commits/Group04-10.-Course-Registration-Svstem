"""Test nghiệp vụ đăng ký học phần (dùng SQLite trong RAM)."""
from app.extensions import db
from app.models import ClassSection, Enrollment
from app.services import registration_service as reg


# --------------------------------------------------------- check_conditions
def test_conditions_ok(data, make_course, make_class):
    c1 = make_class("CL001", make_course("C0001"))
    problems, global_problems = reg.check_conditions(data.term, [], [c1])
    assert problems["CL001"] == []
    assert global_problems == []


def test_conditions_registration_closed(data, make_course, make_class):
    c1 = make_class("CL001", make_course("C0001"))
    data.term.status = "CLOSED"
    db.session.commit()
    _, global_problems = reg.check_conditions(data.term, [], [c1])
    assert "Registration is not open" in global_problems


def test_conditions_class_full(data, make_course, make_class):
    full = make_class("CL001", make_course("C0001"), capacity=1, enrolled=1)
    problems, _ = reg.check_conditions(data.term, [], [full])
    assert "Class is full" in problems["CL001"]


def test_conditions_schedule_conflict(data, make_course, make_class):
    registered = make_class("CL001", make_course("C0001"), hour=8)
    clash = make_class("CL002", make_course("C0002"), hour=8)
    problems, _ = reg.check_conditions(data.term, [registered], [clash])
    assert any("Schedule conflict" in e for e in problems["CL002"])


def test_conditions_same_course_other_section_already_registered(data, make_course, make_class):
    course = make_course("C0001")
    registered = make_class("CL001", course, hour=8)
    other = make_class("CL002", course, hour=10)
    problems, _ = reg.check_conditions(data.term, [registered], [other])
    assert "Already registered for this course in another section" in problems["CL002"]


def test_conditions_two_sections_of_same_course_in_cart(data, make_course, make_class):
    course = make_course("C0001")
    a = make_class("CL001", course, hour=8)
    b = make_class("CL002", course, hour=10)
    problems, _ = reg.check_conditions(data.term, [], [a, b])
    assert "Another section of this course is also selected" in problems["CL002"]


def test_conditions_credit_limit(app, data, make_course, make_class):
    app.config["MAX_CREDITS"] = 5
    a = make_class("CL001", make_course("C0001", credits=3), hour=8)
    b = make_class("CL002", make_course("C0002", credits=3), hour=10)
    _, global_problems = reg.check_conditions(data.term, [], [a, b])
    assert any("exceed the limit of 5" in p for p in global_problems)


# --------------------------------------------------------------- can_select
def test_can_select_ok(data, make_course, make_class):
    make_class("CL001", make_course("C0001"))
    ok, _ = reg.can_select("S0001", "CL001", [])
    assert ok is True


def test_can_select_unknown_class(data):
    assert reg.can_select("S0001", "CL999", []) == (False, "Class not found")


def test_can_select_already_in_cart(data, make_course, make_class):
    make_class("CL001", make_course("C0001"))
    assert reg.can_select("S0001", "CL001", ["CL001"]) == (False, "This class is already selected")


# ------------------------------------------------------------------ confirm
def test_confirm_empty_cart(data):
    result = reg.confirm("S0001", [])
    assert result["ok"] is False and result["count"] == 0


def test_confirm_success_creates_enrollment_and_updates_count(data, make_course, make_class):
    make_class("CL001", make_course("C0001"))
    result = reg.confirm("S0001", ["CL001"])
    assert result == {"ok": True, "messages": [], "count": 1}

    enrollment = Enrollment.query.one()
    assert (enrollment.student_id, enrollment.class_id, enrollment.status) == ("S0001", "CL001", "ENROLLED")
    assert db.session.get(ClassSection, "CL001").current_enrollment == 1


def test_confirm_is_all_or_nothing(data, make_course, make_class):
    make_class("CL001", make_course("C0001"), hour=8)
    make_class("CL002", make_course("C0002"), hour=10, capacity=1, enrolled=1)   # lớp đầy

    result = reg.confirm("S0001", ["CL001", "CL002"])

    assert result["ok"] is False
    assert Enrollment.query.count() == 0
    assert db.session.get(ClassSection, "CL001").current_enrollment == 0


# ------------------------------------------------------------------- cancel
def test_cancel_success(data, make_course, make_class):
    make_class("CL001", make_course("C0001"))
    reg.confirm("S0001", ["CL001"])

    ok, _ = reg.cancel("S0001", "CL001")

    assert ok is True
    assert Enrollment.query.count() == 0
    assert db.session.get(ClassSection, "CL001").current_enrollment == 0


def test_cancel_not_registered(data, make_course, make_class):
    make_class("CL001", make_course("C0001"))
    assert reg.cancel("S0001", "CL001") == (False, "You are not registered for this class")


def test_cancel_when_registration_closed(data, make_course, make_class):
    make_class("CL001", make_course("C0001"))
    reg.confirm("S0001", ["CL001"])
    data.term.status = "CLOSED"
    db.session.commit()
    assert reg.cancel("S0001", "CL001") == (False, "Registration is not open")
