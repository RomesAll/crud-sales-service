from sqlalchemy import create_engine, Engine, text
from sqlalchemy.orm import sessionmaker
from app.config import config

def health_check_connection(engine: Engine):
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
            config.logging.app.info("Соединение с БД установлено!")
            return True
    except Exception as e:
        config.logging.app.fatal(f"Ошибка соединения с БД: {e}")
        return False

engine = create_engine(
    url=config.postgres.url,
    echo=True,
    pool_size=5,
    max_overflow=10
)
session_maker = sessionmaker(bind=engine, expire_on_commit=True)
health_check_connection(engine)