from sqlalchemy import event
from app.data.models.base import Base
from app.data.models.sale import Sale

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

def generate_slug(text: str) -> str:
    text = text.upper()
    for char in text:
        if char.isalpha() and char in mapping_dict_alph:
            text = text.replace(char, mapping_dict_alph[char])
    return text.lower()

def checking_column_exist(column: tuple):
    name, target = column
    return name in target.__table__.columns

@event.listens_for(Base, 'before_insert')
def generate_slug_before_insert(mapper, connection, target):
    is_column_exist = all(map(checking_column_exist, [('slug', target), ('name', target)]))
    if not is_column_exist:
        target.slug = generate_slug(target.name)

@event.listens_for(Sale, 'before_insert')
@event.listens_for(Sale, 'before_update')
def calculation_total(mapper, connection, target: Sale):
    target._total_amount = target.total_amount