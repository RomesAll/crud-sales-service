from sqlalchemy import MetaData, event
from sqlalchemy.orm import DeclarativeBase

columns = list[str]

class Base(DeclarativeBase):
    __abstract__ = True
    metadata = MetaData()

    def __repr__(self):
        return f'<{self.__class__.__name__}>(id={getattr(self, "category_id", None)})'

    def to_dict(self, exclude: columns | None = None):
        result = {}
        for column in self.__table__.columns.keys():
            data = getattr(self, column)
            if exclude and column in exclude:
                continue
            result.update({column: data})
        return result

def generate_slug(text: str) -> str:
    text = text.upper()
    for char in text:
        if char.isalpha() and char in mapping_dict_alph:
            text = text.replace(char, mapping_dict_alph[char])
    return text.lower()
