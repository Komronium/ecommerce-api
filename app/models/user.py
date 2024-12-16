from uuid import uuid4
from sqlalchemy import Column, Uuid, String, Boolean
from app.core.security import hash_password
from app.db.base import Base


class User(Base):
    id = Column(Uuid(as_uuid=True), primary_key=True, default=uuid4, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)

    def set_password(self, password: str):
        self.hashed_password = hash_password(password)
