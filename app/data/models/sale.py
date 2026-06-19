import datetime
from sqlalchemy import ForeignKey, String, DateTime, event
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base
from app.data.mixins import UUIDMixin, TimestampMixin

class Sale(UUIDMixin, Base):
    __tablename__ = 'sales'
    product_id: Mapped[int] = mapped_column(
        ForeignKey('products.id', ondelete='SET NULL'),
    )
    sale_date: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )
    quantity: Mapped[int] = mapped_column(
        default=0,
    )
    unit_price: Mapped[float] = mapped_column(
        default=0.0
    )
    discount: Mapped[int] = mapped_column(
        default=0,
    )
    _total_amount: Mapped[float] = mapped_column(
        default=0,
    )
    customer_id: Mapped[int] = mapped_column(
        default=0,
    )
    sales_channel: Mapped[str] = mapped_column(
        String(50)
    )

    @property
    def total_amount(self):
        return self.quantity * self.unit_price * (1 - self.discount/100)

    @total_amount.setter
    def total_amount(self, value):
        raise ValueError("Поле 'total_amount' вычисляемое, поэтому напрямую присваивать значение нельзя")

@event.listens_for(Sale, 'before_insert')
@event.listens_for(Sale, 'before_update')
def calculation_total(mapper, connection, target: Sale):
    target._total_amount = target.total_amount