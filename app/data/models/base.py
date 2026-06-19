from sqlalchemy import MetaData
from sqlalchemy.orm import DeclarativeBase
from app.data.mixins import TimestampMixin

columns = list[str]

class Base(TimestampMixin, DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()

    def __repr__(self):
        id = getattr(self, "id", None)
        uuid = getattr(self, "uuid", None)
        name = getattr(self, "name", None)
        return f'<{self.__class__.__name__}>(id={id if id else uuid}, name={name})'

    def to_dict(self, exclude: columns | None = None):
        result = {}
        for column in self.__table__.columns.keys():
            data = getattr(self, column)
            if exclude and column in exclude:
                continue
            result.update({column: data})
        return result