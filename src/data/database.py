from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.config import config

engine = create_engine(
    url=config.postgres.url,
    echo=True,
    pool_size=5,
    max_overflow=10
)

session_maker = sessionmaker(bind=engine)