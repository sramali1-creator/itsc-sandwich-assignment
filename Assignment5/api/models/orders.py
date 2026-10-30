from sqlalchemy import Column, DATETIME, Integer, String, func
from sqlalchemy.orm import relationship

from ..dependencies.database import Base


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    customer_name = Column(String(100), nullable=False)
    order_date = Column(DATETIME, nullable=False, server_default=func.now())
    description = Column(String(300))

    order_details = relationship("OrderDetail", back_populates="order")
