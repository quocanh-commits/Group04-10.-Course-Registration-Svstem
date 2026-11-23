from app.services.schedule_utils import schedule_label


def to_view(cls, status=""):
    """Chuyển ClassSection thành dict cho template."""
    return {
        "class_id": cls.id,
        "course_id": cls.course_id,
        "name": cls.course.title,
        "lecturer": cls.lecturer.full_name,
        "credits": cls.course.credits,
        "schedule": schedule_label(cls.schedule_time),
        "room": f"Room {(cls.room or '').strip()}",
        "enrolled": cls.current_enrollment,
        "capacity": cls.max_capacity,
        "status": status,
    }
