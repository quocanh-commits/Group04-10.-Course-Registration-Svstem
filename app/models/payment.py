from app.extensions import db


class Payment(db.Model):
    __tablename__ = "payment"

    id = db.Column("transactionid", db.Integer, primary_key=True)   # UML gọi là paymentId
    amount = db.Column("amount", db.Float, nullable=False)
    payment_date = db.Column("paymentdate", db.Date, nullable=False)
    status = db.Column("status", db.String(100), nullable=False)
    student_id = db.Column("studentid", db.String(5), db.ForeignKey("student.studentid"), nullable=False)
