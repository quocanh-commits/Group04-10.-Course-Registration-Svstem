from datetime import date

from flask import current_app
from sqlalchemy.exc import SQLAlchemyError

from app.extensions import db
from app.models.enrollment import Enrollment
from app.repositories import class_repository, enrollment_repository, term_repository
from app.services.class_view import to_view
from app.services.schedule_utils import slot_key


# ---------------------------------------------------------------- điều kiện
def check_conditions(term, registered, candidates):
    """Check Course Conditions. Trả (lỗi theo từng lớp, lỗi chung)."""
    problems = {c.id: [] for c in candidates}
    global_problems = []

    if term is None or not term.is_registration_open():
        global_problems.append("Registration is not open")

    max_credits = current_app.config["MAX_CREDITS"]
    registered_ids = {c.id for c in registered}
    registered_courses = {c.course_id for c in registered}
    occupied = {slot_key(c.schedule_time): c for c in registered}
    seen_courses = set()
    new_credits = 0

    for cand in candidates:
        errs = problems[cand.id]
        if term is not None and cand.term_id != term.id:
            errs.append("Not part of the current registration term")
        if cand.id in registered_ids:
            errs.append("Already registered for this class")
        elif cand.course_id in registered_courses:
            errs.append("Already registered for this course in another section")
        if cand.course_id in seen_courses:
            errs.append("Another section of this course is also selected")
        if cand.id not in registered_ids and cand.current_enrollment >= cand.max_capacity:
            errs.append("Class is full")
        clash = occupied.get(slot_key(cand.schedule_time))
        if clash is not None and clash.id != cand.id:
            errs.append(f"Schedule conflict with {clash.course.title} ({clash.id})")

        seen_courses.add(cand.course_id)
        if not errs:
            occupied[slot_key(cand.schedule_time)] = cand
            new_credits += cand.course.credits

    total = sum(c.course.credits for c in registered) + new_credits
    if total > max_credits:
        global_problems.append(f"Total credits {total} exceed the limit of {max_credits}")
    return problems, global_problems


# ------------------------------------------------------------ chọn (tạm thời)
def can_select(student_id, class_id, cart_ids):
    """Kiểm tra khi bấm Select. Chỉ cho vào giỏ tạm, không ghi database."""
    term = term_repository.get_current_term()
    cls = class_repository.get(class_id)
    if cls is None:
        return False, "Class not found"
    if class_id in cart_ids:
        return False, "This class is already selected"

    registered = class_repository.find_registered(student_id, term.id) if term else []
    others = class_repository.get_many(cart_ids)
    problems, global_problems = check_conditions(term, registered, others + [cls])
    errors = problems[cls.id] + global_problems
    if errors:
        return False, f"{cls.course.title} ({cls.id}): " + "; ".join(errors)
    return True, f"Selected {cls.course.title} ({cls.id})"


# ---------------------------------------------------------- trang đăng ký
def build_plan(student_id, cart_ids):
    term = term_repository.get_current_term()
    registered = class_repository.find_registered(student_id, term.id) if term else []
    candidates = class_repository.get_many(cart_ids)
    problems, global_problems = check_conditions(term, registered, candidates)

    cart_rows = []
    for c in candidates:
        row = to_view(c, "Selected")
        row["problems"] = problems[c.id]
        row["ok"] = not problems[c.id]
        cart_rows.append(row)

    registered_rows = [to_view(c, "Registered") for c in registered]
    total_credits = (sum(c.course.credits for c in registered)
                     + sum(c.course.credits for c in candidates))
    all_valid = bool(candidates) and not global_problems and all(r["ok"] for r in cart_rows)

    return {
        "term": term,
        "registered_rows": registered_rows,
        "cart_rows": cart_rows,
        "cart_ids": [c.id for c in candidates],   # bỏ mã lớp không còn tồn tại
        "total_credits": total_credits,
        "global_problems": global_problems,
        "all_valid": all_valid,
    }


# ------------------------------------------------------- xác nhận (ghi DB)
def confirm(student_id, cart_ids):
    """Choose to register for a class (DFD 4.0). Tất cả hoặc không gì cả."""
    if not cart_ids:
        return {"ok": False, "messages": ["No classes selected"], "count": 0}

    term = term_repository.get_current_term()
    classes = class_repository.get_many(cart_ids, lock=True)   # khóa dòng, tránh vượt sĩ số
    registered = class_repository.find_registered(student_id, term.id) if term else []

    problems, global_problems = check_conditions(term, registered, classes)
    messages = list(global_problems)
    for c in classes:
        for err in problems[c.id]:
            messages.append(f"{c.course.title} ({c.id}): {err}")
    if messages:
        db.session.rollback()   # nhả khóa, chưa ghi gì
        return {"ok": False, "messages": messages, "count": 0}

    try:
        number = enrollment_repository.next_id_number()
        for c in classes:
            enrollment_repository.add(Enrollment(
                id=enrollment_repository.format_id(number),
                enrolled_at=date.today(),
                status="ENROLLED",
                class_id=c.id,
                student_id=student_id,
            ))
            c.current_enrollment += 1
            number += 1
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Register failed")
        return {"ok": False, "messages": ["Could not save the registration. Please try again."],
                "count": 0}

    return {"ok": True, "messages": [], "count": len(classes)}


# ------------------------------------------------------------------- hủy
def cancel(student_id, class_id):
    term = term_repository.get_current_term()
    if term is None or not term.is_registration_open():
        return False, "Registration is not open"

    enrollment = enrollment_repository.find(student_id, class_id)
    if enrollment is None:
        return False, "You are not registered for this class"

    try:
        cls = class_repository.get(class_id, lock=True)
        enrollment_repository.delete(enrollment)
        cls.current_enrollment = max(0, cls.current_enrollment - 1)
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        current_app.logger.exception("Cancel failed")
        return False, "Could not cancel the registration. Please try again."
    return True, f"Cancelled registration for {cls.course.title} ({cls.id})"
