from app.repositories import (class_repository, course_repository, enrollment_repository,
                              term_repository, user_repository, wishlist_repository)


def get_overview():
    term = term_repository.get_current_term()
    return {
        "term_name": term.name if term else "—",
        "registration_open": bool(term and term.is_registration_open()),
        "students": user_repository.count("student"),
        "lecturers": user_repository.count("lecturer"),
        "admins": user_repository.count("admin"),
        "courses": course_repository.count(),
        "classes": class_repository.count_by_term(term.id) if term else 0,
        "enrollments": enrollment_repository.count_by_term(term.id) if term else 0,
        "pending_wishlist": wishlist_repository.count_by_status("PENDING"),
    }
