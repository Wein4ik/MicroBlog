import enum

from datetime import datetime

from sqlalchemy import ForeignKey, String, func, Integer, DateTime, UniqueConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
)

from config import USERNAME_MAX_LENGTH_DEFAULT


class Base(DeclarativeBase):
    pass


class ContentType(enum.Enum):
    POST = 'post'
    COMMENT = 'comment'


class Like(Base):
    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint('user_id', 'content_id', name='unique_user_content_like'),
    )

    id = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    content_id: Mapped[int] = mapped_column(ForeignKey("contents.id"), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="likes")
    content: Mapped["Content"] = relationship("Content", back_populates="likes")

    def dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content_id': self.content_id
        }


class User(Base):
    __tablename__ = "users"

    id = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(USERNAME_MAX_LENGTH_DEFAULT), index=True, unique=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    contents: Mapped[list["Content"]] = relationship('Content', back_populates='user')
    likes: Mapped[list["Like"]] = relationship('Like', back_populates='user')

    def dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'created_at': self.created_at
        }


class Content(Base):
    __tablename__ = "contents"

    id = mapped_column(Integer, primary_key=True)
    content: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    content_type: Mapped[ContentType]

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), index=True)
    parent_id: Mapped[int] = mapped_column(ForeignKey('contents.id'), nullable=True, index=True)

    likes: Mapped[list["Like"]] = relationship('Like', back_populates='content', cascade="all, delete")
    user: Mapped["User"] = relationship('User', back_populates='contents')
    comments: Mapped[list["Content"]] = relationship("Content", back_populates="parent", cascade="all, delete")
    #children = relationship("Content", back_populates="parent", cascade="all, delete")
    parent: Mapped["Content"] = relationship("Content", back_populates="comments", remote_side=[id])

    def dict(self):
        return {
            'id': self.id,
            'content': self.content,
            'created_at': self.created_at,
            'content_type': self.content_type,
            'user_id': self.user_id,
            'parent_id': self.parent_id
        }
