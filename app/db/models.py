from datetime import datetime
from sqlalchemy import Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)
    hash_pwd: Mapped[str|None] = mapped_column(String(128), nullable=False)
    role: Mapped[str] = mapped_column(String, default='user')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Связь с сообщениями
    messages: Mapped[list["ChatMessage"]] = relationship(back_populates="user")

class ChatMessage(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    role: Mapped[str] = mapped_column(String, default='user')
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

    # Связь с пользователем
    user: Mapped["User"] = relationship(back_populates="messages")