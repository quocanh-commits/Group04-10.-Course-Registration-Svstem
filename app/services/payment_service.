from flask import current_app

from app.models import Payment
from app.repositories import enrollment_repository, term_repository
from app.repositories import payment_repository as repo
from app.services.result import PaymentResult as R


def tuition_summary(student_id):
    term = term_repository.get_open_term() or term_repository.get_latest_term()
    if not term:
        return None
    ens = enrollment_repository.active_in_term(student_id, term.term_id)
    credits = sum(e.class_section.course.credits for e in ens)
    total = credits * current_app.config["TUITION_PER_CREDIT"]
    paid = repo.total_paid(student_id, term.term_id)
    return {"term": term, "credits": credits, "total": total, "paid": paid,
            "remaining": max(total - paid, 0), "payments": repo.list_by_student(student_id)}


def make_payment(student_id):
    s = tuition_summary(student_id)
    if not s or s["remaining"] <= 0:
        return R(False, "There is no tuition to pay.")

    payment = repo.save(Payment(student_id=student_id, term_id=s["term"].term_id,
                                amount=s["remaining"]))
    result = current_app.extensions["billing_system"].charge(
        student_id, payment.amount, payment.payment_id)

    payment.status = "SUCCESS" if result.success else "FAILED"
    payment.transaction_ref = result.transaction_ref
    repo.save(payment)

    if result.success:
        return R(True, f"Payment of {payment.amount:,} VND successful.", payment)
    return R(False, f"Payment failed: {result.message}", payment)
