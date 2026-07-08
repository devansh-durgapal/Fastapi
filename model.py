from database import Base
from sqlalchemy.orm import mapped_column, Mapped, relationship
from sqlalchemy import DateTime, String, ForeignKey

class UserData(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True)
    name: Mapped[str | None] = mapped_column(String(50), default=None, nullable=True)
    email: Mapped[str] = mapped_column(unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[str] = mapped_column(String(20), default="user")