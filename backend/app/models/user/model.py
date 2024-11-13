from typing import Optional
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from pydantic import BaseModel

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(50))
    hashed_password: Mapped[str] = mapped_column(String(500))
    refresh_token: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)