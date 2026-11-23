from app.models.registration_term import RegistrationTerm
from app.repositories import term_repository
from app.services.errors import ServiceError, commit, parse_date


def _fmt(d):
    return d.strftime("%d/%m/%Y") if d else ""


def list_terms():
    counts = term_repository.class_counts()
    return [{
        "id": t.id,
        "name": t.name,
        "period": f"{_fmt(t.start_date)} – {_fmt(t.end_date)}",
        "window": f"{_fmt(t.registration_open)} – {_fmt(t.registration_close)}",
        "classes": counts.get(t.id, 0),
        "status": (t.status or "").strip().upper(),
    } for t in term_repository.list_all()]


def form_values(term_id):
    t = term_repository.get(term_id)
    if t is None:
        return None
    return {
        "term_id": t.id, "semester_name": t.name,
        "start_date": t.start_date.isoformat(), "end_date": t.end_date.isoformat(),
        "registration_open": t.registration_open.isoformat(),
        "registration_close": t.registration_close.isoformat(),
    }


def _clean(form):
    name = (form.get("semester_name") or "").strip()
    if not name or len(name) > 10:
        raise ServiceError("Semester name is required (max 10 characters, e.g. HK2 26-27)")
    start = parse_date(form.get("start_date"), "Start date")
    end = parse_date(form.get("end_date"), "End date")
    reg_open = parse_date(form.get("registration_open"), "Registration opens")
    reg_close = parse_date(form.get("registration_close"), "Registration closes")
    if start >= end:
        raise ServiceError("Start date must be before the end date")
    if reg_open > reg_close:
        raise ServiceError("Registration cannot close before it opens")
    return name, start, end, reg_open, reg_close


def create_term(admin_id, form):
    name, start, end, reg_open, reg_close = _clean(form)
    term_id = f"TERM{start:%Y%m}"
    if term_repository.get(term_id):
        raise ServiceError(f"A term starting in {start:%m/%Y} already exists ({term_id})")
    term_repository.add(RegistrationTerm(
        id=term_id, semester_name=name, start_date=start, end_date=end,
        registration_open=reg_open, registration_close=reg_close,
        status="PLANNED", admin_id=admin_id))
    commit()
    return f"Created term {term_id} ({name}) with status PLANNED"


def update_term(term_id, form):
    term = term_repository.get(term_id)
    if term is None:
        raise ServiceError("Term not found")
    (term.semester_name, term.start_date, term.end_date,
     term.registration_open, term.registration_close) = _clean(form)
    commit()
    return f"Updated term {term_id}"


def open_registration(term_id):
    """openRegistrationTerm: chỉ một học kỳ OPEN tại một thời điểm."""
    term = term_repository.get(term_id)
    if term is None:
        raise ServiceError("Term not found")
    for other in term_repository.open_terms():
        if other.id != term_id:
            other.status = "CLOSED"
    term.status = "OPEN"
    commit()
    return f"Registration for {term.name} is now OPEN (other open terms were closed)"


def close_registration(term_id):
    term = term_repository.get(term_id)
    if term is None:
        raise ServiceError("Term not found")
    term.status = "CLOSED"
    commit()
    return f"Registration for {term.name} is now CLOSED"


def delete_term(term_id):
    term = term_repository.get(term_id)
    if term is None:
        raise ServiceError("Term not found")
    n = term_repository.class_counts().get(term_id, 0)
    if n:
        raise ServiceError(f"Cannot delete {term_id}: it still has {n} class section(s)")
    term_repository.delete(term)
    commit()
    return f"Deleted term {term_id}"


def term_options():
    return [{"id": t.id, "name": t.name, "status": (t.status or "").strip().upper()}
            for t in term_repository.list_all()]
