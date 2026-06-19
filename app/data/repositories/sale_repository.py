from datetime import date, datetime, timezone
from sqlalchemy import select
from .base import BaseRepositoryORM
from ..models import Sale
import pytz

class SaleRepository(BaseRepositoryORM):
    model = Sale

    def get_sale_date(self, current_date: date, time_zone: str = "America/New_York"):
        tz = pytz.timezone(time_zone)
        local_start = datetime(current_date.year, current_date.month, current_date.day, 0, 0, 0)
        local_end = datetime(current_date.year, current_date.month, current_date.day, 23, 59, 59)
        utc_start = tz.localize(local_start).astimezone(timezone.utc)
        utc_end = tz.localize(local_end).astimezone(timezone.utc)
        stmt = select(Sale).filter(Sale.sale_date.between(utc_start, utc_end))
        sales = self.session.execute(stmt).scalars().all()
        return sales

    def get_customer(self, customer_id: int):
        stmt = select(Sale).where(Sale.customer_id == customer_id)
        sales = self.session.execute(stmt).scalars().all()
        return sales