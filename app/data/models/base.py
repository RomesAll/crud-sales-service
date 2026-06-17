from sqlalchemy import MetaData, event
from sqlalchemy.orm import DeclarativeBase

columns = list[str]

mapping_dict_alph = {
    'А' : 'A',
    'Б' : 'B',
    'В' : 'V',
    'Г' : 'G',
    'Д' : 'D',
    'Е' : 'E',
    'Ё' : 'E',
    'Ж' : 'ZH',
    'З' : 'Z',
    'И' : 'I',
    'Й' : 'I',
    'К' : 'K',
    'Л' : 'L',
    'М' : 'M',
    'Н' : 'N',
    'О' : 'O',
    'П' : 'P',
    'Р' : 'R',
    'С' : 'S',
    'Т' : 'T',
    'У' : 'U',
    'Ф' : 'F',
    'Х' : 'KH',
    'Ц' : 'TS',
    'Ч' : 'CH',
    'Ш' : 'SH',
    'Щ' : 'SHCH',
    'Ы' : 'Y',
    'Э' : 'E',
    'Ю' : 'IU',
    'Я' : 'IA',
}

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
