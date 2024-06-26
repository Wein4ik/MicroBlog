import enum

from datetime import datetime

from sqlalchemy import ForeignKey, String, func, Integer, DateTime
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)


class Base(DeclarativeBase):
    pass


class ContentType(enum.Enum):
    POST = 'post'
    COMMENT = 'comment'


class Like(Base):
    __tablename__ = "likes"

    id = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content_id: Mapped[int] = mapped_column(ForeignKey("contents.id"))

    user: Mapped["User"] = relationship("User", back_populates="likes")
    content: Mapped["Content"] = relationship("Content", back_populates="likes")


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(20), index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    contents: Mapped[list["Content"]] = relationship('Content', back_populates='user')
    likes: Mapped[list["Like"]] = relationship('Like', back_populates='user')


class Content(Base):
    __tablename__ = "contents"

    id = mapped_column(Integer, primary_key=True)
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    content_type: Mapped[ContentType]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('contents.id'), nullable=True, index=True)

    likes: Mapped[list["Like"]] = relationship('Like', back_populates='content')
    user: Mapped["User"] = relationship('User', back_populates='contents')
    comments: Mapped[list["Content"]] = relationship("Content", back_populates="parent")
    parent: Mapped["Content"] = relationship("Content", back_populates="comments", remote_side=[id])
