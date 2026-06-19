from sqlalchemy import DateTime, func, UUID, Uuid
from sqlalchemy.orm import Mapped, mapped_column
import uuid, datetime

class IdMixin:
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        index=True
    )

class UUIDMixin:
    uuid: Mapped[UUID] = mapped_column(
        Uuid,
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )

class TimestampMixin:
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(tz=datetime.timezone.utc),
        server_default=func.now(),
        index=True,
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.datetime.now(tz=datetime.timezone.utc),
        server_default = func.now()
    )

class SlugMixin:
    slug: Mapped[str] = mapped_column(
        unique=True,
        index=True
    )