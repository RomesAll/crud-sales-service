from sqlalchemy import ForeignKey, String
from app.data.models.mixins import IdMixin, SlugMixin, TimestampMixin
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

class Category(IdMixin, SlugMixin, TimestampMixin, Base):
    __tablename__ = 'categories'
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True
    )
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )
    parent_category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='SET NULL'),
        nullable=True
    )