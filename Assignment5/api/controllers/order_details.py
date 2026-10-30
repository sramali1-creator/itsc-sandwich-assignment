from fastapi import HTTPException, Response, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import order_details as model
from ..models.orders import Order
from ..models.sandwiches import Sandwich


def _db_error(e: SQLAlchemyError):
    if isinstance(e, IntegrityError):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid order_id or sandwich_id")
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__.get("orig", e)))


def _check_refs(db: Session, order_id=None, sandwich_id=None):
    if order_id is not None and not db.query(Order).filter(Order.id == order_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Order {order_id} not found")
    if sandwich_id is not None and not db.query(Sandwich).filter(Sandwich.id == sandwich_id).first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Sandwich {sandwich_id} not found")


def create(db: Session, request):
    _check_refs(db, request.order_id, request.sandwich_id)
    new_item = model.OrderDetail(
        order_id=request.order_id,
        sandwich_id=request.sandwich_id,
        amount=request.amount,
    )
    try:
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
    except SQLAlchemyError as e:
        db.rollback()
        _db_error(e)
    return new_item


def read_all(db: Session):
    try:
        return db.query(model.OrderDetail).all()
    except SQLAlchemyError as e:
        _db_error(e)


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id).first()
    except SQLAlchemyError as e:
        _db_error(e)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail not found")
    return item


def update(db: Session, item_id: int, request):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail not found")
    update_data = request.model_dump(exclude_unset=True)
    _check_refs(db, update_data.get("order_id"), update_data.get("sandwich_id"))
    try:
        if update_data:
            item.update(update_data, synchronize_session=False)
            db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        _db_error(e)
    return item.first()


def delete(db: Session, item_id: int):
    item = db.query(model.OrderDetail).filter(model.OrderDetail.id == item_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order detail not found")
    try:
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        _db_error(e)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
