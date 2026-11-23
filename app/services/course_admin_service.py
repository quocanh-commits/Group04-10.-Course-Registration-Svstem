from datetime import datetime

from app.models.class_section import ClassSection
from app.models.course import Course
from app.repositories import class_repository, course_repository, term_repository, user_repository
from app.services.errors import ServiceError, commit, parse_int
from app.services.schedule_utils import VN_TZ, slot_key, to_local


# ----------------------------------------------------------------- course
def list_courses():
    counts = course_repository.class_counts()
    return [{"id": c.id, "title": c.title, "credits": c.credits,
             "classes": counts.get(c.id, 0)} for c in course_repository.list_all()]


def course_form_values(course_id):
    c = course_repository.get(course_id)
    return None if c is None else {"course_id": c.id, "title": c.title, "credits": c.credits}


def _clean_course(form, exclude_id=None):
    title = (form.get("title") or "").strip()
    if not title or len(title) > 100:
        raise ServiceError("Course title is required (max 100 characters)")
    if course_repository.title_exists(title, exclude_id):
        raise ServiceError("A course with this title already exists")
    credits = parse_int(form.get("credits"), "Credits", 1, 15)
    return title, credits


def create_course(admin_id, form):
    title, credits = _clean_course(form)
    course = Course(id=course_repository.next_id(), title=title, credits=credits, admin_id=admin_id)
    course_repository.add(course)
    commit()
    return f"Created course {course.id} · {title}"


def update_course(course_id, form):
    course = course_repository.get(course_id)
    if course is None:
        raise ServiceError("Course not found")
    course.title, course.credits = _clean_course(form, exclude_id=course_id)
    commit()
    return f"Updated course {course_id}"


def delete_course(course_id):
    course = course_repository.get(course_id)
    if course is None:
        raise ServiceError("Course not found")
    n = course_repository.count_classes(course_id)
    if n:
        raise ServiceError(f"Cannot delete {course_id}: it still has {n} class section(s)")
    course_repository.delete(course)
    commit()
    return f"Deleted course {course_id}"


# ---------------------------------------------------------- class section
def _fmt(dt):
    local = to_local(dt)
    return local.strftime("%d/%m/%Y %H:%M") if local else ""


def list_classes(term_id):
    return [{
        "id": c.id,
        "course_id": c.course_id,
        "title": c.course.title,
        "credits": c.course.credits,
        "lecturer_id": c.lecturer_id,
        "lecturer": c.lecturer.full_name,
        "room": (c.room or "").strip(),
        "schedule": _fmt(c.schedule_time),
        "capacity": c.max_capacity,
        "enrolled": c.current_enrollment,
    } for c in class_repository.list_by_term(term_id)]


def class_form_values(class_id):
    c = class_repository.get(class_id)
    if c is None:
        return None
    local = to_local(c.schedule_time)
    return {
        "class_id": c.id, "course_id": c.course_id, "course_title": c.course.title,
        "lecturer_id": c.lecturer_id, "room": (c.room or "").strip(),
        "capacity": c.max_capacity,
        "schedule_time": local.strftime("%Y-%m-%dT%H:%M") if local else "",
        "term_id": c.term_id, "enrolled": c.current_enrollment,
    }


def _parse_schedule(value):
    try:
        return datetime.fromisoformat((value or "").strip()).replace(tzinfo=VN_TZ)
    except ValueError:
        raise ServiceError("Schedule time is not a valid date and time")


def _check_conflicts(term_id, lecturer_id, room, when, exclude_id=None):
    key = slot_key(when)
    for other in class_repository.by_lecturer_in_term(term_id, lecturer_id):
        if other.id != exclude_id and slot_key(other.schedule_time) == key:
            raise ServiceError(f"The lecturer already teaches {other.id} at that time")
    for other in class_repository.by_room_in_term(term_id, room):
        if other.id != exclude_id and slot_key(other.schedule_time) == key:
            raise ServiceError(f"Room {room} is already used by {other.id} at that time")


def _clean_common(form):
    lecturer_id = (form.get("lecturer_id") or "").strip()
    if user_repository.find_by_id("lecturer", lecturer_id) is None:
        raise ServiceError("Please choose a lecturer")
    room = (form.get("room") or "").strip().upper()
    if not room.isalnum() or len(room) > 4:
        raise ServiceError("Room must be 1-4 letters or digits, e.g. B401")
    capacity = parse_int(form.get("capacity"), "Capacity", 1, 500)
    when = _parse_schedule(form.get("schedule_time"))
    return lecturer_id, room, capacity, when


def create_class(form):
    term = term_repository.get((form.get("term_id") or "").strip())
    if term is None:
        raise ServiceError("Please choose a semester")
    course_id = (form.get("course_id") or "").strip()
    if course_repository.get(course_id) is None:
        raise ServiceError("Please choose a course")
    lecturer_id, room, capacity, when = _clean_common(form)
    _check_conflicts(term.id, lecturer_id, room, when)

    class_id, number = class_repository.next_id()
    if number > 999:
        raise ServiceError("No more class codes available")
    class_repository.add(ClassSection(
        id=class_id, current_enrollment=0, schedule_time=when, room=room,
        max_capacity=capacity, term_id=term.id, course_id=course_id, lecturer_id=lecturer_id))
    commit()
    return f"Created class section {class_id}"


def update_class(class_id, form):
    cls = class_repository.get(class_id)
    if cls is None:
        raise ServiceError("Class section not found")
    lecturer_id, room, capacity, when = _clean_common(form)
    if capacity < cls.current_enrollment:
        raise ServiceError(f"Capacity cannot be lower than the {cls.current_enrollment} enrolled students")
    _check_conflicts(cls.term_id, lecturer_id, room, when, exclude_id=class_id)
    cls.lecturer_id, cls.room, cls.max_capacity, cls.schedule_time = lecturer_id, room, capacity, when
    commit()
    return f"Updated class section {class_id}"


def delete_class(class_id):
    cls = class_repository.get(class_id)
    if cls is None:
        raise ServiceError("Class section not found")
    n = class_repository.enrollment_count(class_id)
    if n:
        raise ServiceError(f"Cannot delete {class_id}: {n} student(s) are enrolled")
    class_repository.delete(cls)
    commit()
    return f"Deleted class section {class_id}"


def lecturer_options():
    return [{"id": l.id, "name": l.full_name} for l in user_repository.list_users("lecturer")]


def course_options():
    return [{"id": c.id, "title": c.title, "credits": c.credits} for c in course_repository.list_all()]
