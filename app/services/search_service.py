from app.repositories import (class_repository, course_repository,
                              enrollment_repository, term_repository)
from app.services.class_view import to_view
from app.services.schedule_utils import slot_key


def current_term_info():
    term = term_repository.get_current_term()
    if term is None:
        return None
    return {"id": term.id, "name": term.name, "open": term.is_registration_open()}


def credit_options():
    return course_repository.credit_values()


def search_classes(student_id, cart_ids, keyword="", credits=None, status=""):
    """Search Course, Classes (DFD 3.0). Trạng thái tính theo từng sinh viên."""
    term = term_repository.get_current_term()
    if term is None:
        return []
    classes = class_repository.search(term.id, keyword, credits)
    registered_ids = enrollment_repository.class_ids_of_student(student_id, term.id)

    rows = []
    for c in classes:
        if c.id in registered_ids:
            st = "Registered"
        elif c.id in cart_ids:
            st = "Selected"
        elif c.current_enrollment >= c.max_capacity:
            st = "Full"
        else:
            st = "Available"
        if status and status != "All statuses" and st != status:
            continue
        rows.append(to_view(c, st))
    return rows


def view_schedule(student_id):
    """Các lớp đã đăng ký của học kỳ hiện tại, sắp theo thứ và giờ học."""
    term = term_repository.get_current_term()
    if term is None:
        return []
    classes = class_repository.find_registered(student_id, term.id)
    classes.sort(key=lambda c: slot_key(c.schedule_time))
    return [to_view(c, "Registered") for c in classes]
