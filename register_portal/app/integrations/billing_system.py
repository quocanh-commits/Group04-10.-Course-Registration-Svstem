from abc import ABC, abstractmethod


class BillingSystem(ABC):
    """Interface BillingSystem trong UML. Sẽ dùng ở bước Payment."""

    @abstractmethod
    def verify_payment(self, transaction_details): ...

    @abstractmethod
    def deduct_funds(self, account_id, amount): ...

    @abstractmethod
    def process_refund(self, transaction_id): ...

    @abstractmethod
    def generate_invoice(self, student_id, amount): ...
