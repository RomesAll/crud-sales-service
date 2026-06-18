from datetime import datetime
from typing import Sequence
from sqlalchemy.orm import Session
from app.data.models import Category
from sqlalchemy import select

class CategoryRepository:
    def __init__(self, session: Session):
        self.session = session
