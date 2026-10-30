from fastapi import HTTPException, Response, status
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.orm import Session

from ..models import resources as model


def _db_error(e: SQLAlchemyError):
    if isinstance(e, IntegrityError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Resource item already exists or resource is still used in a recipe",
        )
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e.__dict__.get("orig", e)))


def create(db: Session, request):
    new_item = model.Resource(item=request.item, amount=request.amount)
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
        return db.query(model.Resource).all()
    except SQLAlchemyError as e:
        _db_error(e)


def read_one(db: Session, item_id: int):
    try:
        item = db.query(model.Resource).filter(model.Resource.id == item_id).first()
    except SQLAlchemyError as e:
        _db_error(e)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    return item


def update(db: Session, item_id: int, request):
    item = db.query(model.Resource).filter(model.Resource.id == item_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    update_data = request.model_dump(exclude_unset=True)
    try:
        if update_data:
            item.update(update_data, synchronize_session=False)
            db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        _db_error(e)
    return item.first()


def delete(db: Session, item_id: int):
    item = db.query(model.Resource).filter(model.Resource.id == item_id)
    if not item.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    try:
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        _db_error(e)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
