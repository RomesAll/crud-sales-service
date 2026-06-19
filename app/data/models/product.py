from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped
from .base import Base
from app.data.mixins import IdMixin, SlugMixin, TimestampMixin

class Product(IdMixin, SlugMixin, Base):
    __tablename__ = 'products'
    name: Mapped[str] = mapped_column(
        String(200),
    )
    category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='RESTRICT')
    )
    price: Mapped[float] = mapped_column(
        default=0.0,
        index=True
    )
    stock_quantity: Mapped[int] = mapped_column(
        default=0
    )
    sku: Mapped[str] = mapped_column(
        String(50),
        unique=True,
    )
    is_active: Mapped[bool] = mapped_column(
        default=True
    )
