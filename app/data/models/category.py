from sqlalchemy import ForeignKey, String, event
from app.data.mixins import IdMixin, SlugMixin, TimestampMixin
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column

MAPPING_ALPH = {
    'А' : 'A', 'Б' : 'B', 'В' : 'V',
    'Г' : 'G', 'Д' : 'D', 'Е' : 'E',
    'Ё' : 'E', 'Ж' : 'ZH', 'З' : 'Z',
    'И' : 'I', 'Й' : 'I', 'К' : 'K',
    'Л' : 'L','М' : 'M','Н' : 'N',
    'О' : 'O','П' : 'P','Р' : 'R',
    'С' : 'S','Т' : 'T','У' : 'U','Ф' : 'F',
    'Х' : 'KH','Ц' : 'TS','Ч' : 'CH','Ш' : 'SH',
    'Щ' : 'SHCH','Ы' : 'Y','Э' : 'E',
    'Ю' : 'IU','Я' : 'IA',
}

class Category(IdMixin, SlugMixin, Base):
    __tablename__ = 'categories'
    name: Mapped[str] = mapped_column(
        String(100),
        unique=True,
    )
    parent_category_id: Mapped[int] = mapped_column(
        ForeignKey('categories.id', ondelete='RESTRICT'),
        nullable=True
    )

@event.listens_for(Category, 'before_insert')
def generate_slug_before_insert(mapper, connection, target):
    is_column_exist = all(map(checking_column_exist, [('slug', target), ('name', target)]))
    if is_column_exist:
        target.slug = generate_slug(target.name)


def generate_slug(text: str) -> str:
    text = text.upper()
    for char in text:
        if char.isalpha() and char in MAPPING_ALPH:
            text = text.replace(char, MAPPING_ALPH[char])
    return text.lower()

def checking_column_exist(column: tuple):
    name, target = column
    return name in target.__table__.columns

