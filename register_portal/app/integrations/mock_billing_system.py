from app.integrations.billing_system import BillingSystem


class MockBillingSystem(BillingSystem):
    """Bản giả lập: luôn thành công. Thay bằng cổng thanh toán thật sau này."""

    def verify_payment(self, transaction_details):
        return True

    def deduct_funds(self, account_id, amount):
        return True

    def process_refund(self, transaction_id):
        return True

    def generate_invoice(self, student_id, amount):
        return {"student_id": student_id, "amount": amount}
