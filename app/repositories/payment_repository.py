from sqlalchemy import func
from app.extensions import db
from app.models import Payment

def save(payment):
    db.session.add(payment)
    db.session.commit()
    return payment

def list_by_student(student_id):
    return (Payment.query.filter_by(student_id=student_id)
            .order_by(Payment.created_at.desc()).all())

def total_paid(student_id, term_id):
    total = (db.session.query(func.coalesce(func.sum(Payment.amount), 0))
             .filter(Payment.student_id == student_id, Payment.term_id == term_id,
                     Payment.status == "SUCCESS").scalar())
    return int(total)
