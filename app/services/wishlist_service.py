from app.repositories import wishlist_repository
from app.services.errors import ServiceError, commit

STATUSES = ("PENDING", "APPROVED", "REJECTED")


def list_records(status=None):
    status = status if status in STATUSES else None
    return [{
        "id": r.id,
        "student_id": r.student_id,
        "student": r.student.full_name,
        "course_id": r.course_id,
        "course": r.course.title,
        "credits": r.course.credits,
        "added": r.added_date.strftime("%d/%m/%Y"),
        "status": (r.approval_status or "").strip().upper(),
    } for r in wishlist_repository.list_records(status)]


def counts():
    return {s: wishlist_repository.count_by_status(s) for s in STATUSES}


def review(record_id, decision):
    """Course approval: chỉ duyệt được bản ghi đang PENDING."""
    if decision not in ("APPROVED", "REJECTED"):
        raise ServiceError("Unknown decision")
    record = wishlist_repository.get(record_id)
    if record is None:
        raise ServiceError("Wishlist record not found")
    if (record.approval_status or "").strip().upper() != "PENDING":
        raise ServiceError("This record was already reviewed")
    record.approval_status = decision
    commit()
    return f"{record.student_id} · {record.course.title}: {decision}"
