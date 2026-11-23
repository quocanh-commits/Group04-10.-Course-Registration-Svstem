from sqlalchemy.orm import joinedload

from app.extensions import db
from app.models.wishlist_record import WishlistRecord


def list_records(status=None):
    q = WishlistRecord.query.options(joinedload(WishlistRecord.student),
                                     joinedload(WishlistRecord.course))
    if status:
        q = q.filter(db.func.upper(db.func.trim(WishlistRecord.approval_status)) == status)
    return q.order_by(WishlistRecord.added_date, WishlistRecord.id).all()


def get(record_id):
    return db.session.get(WishlistRecord, record_id)


def count_by_status(status):
    return (WishlistRecord.query
            .filter(db.func.upper(db.func.trim(WishlistRecord.approval_status)) == status)
            .count())
