from app.db.base import Base
from app.db.session import engine


async def init_db():
    Base.metadata.create_all(bind=engine)
