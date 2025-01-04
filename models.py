"""SQLAlchemy models for the application."""

from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column, relationship


class Base(MappedAsDataclass, DeclarativeBase):
    """Base class for all models."""


class Mixin(MappedAsDataclass):
    """Mixin for all models."""


class IdMixin(Mixin):
    """Mixin for all models with an id."""

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class User(Base, IdMixin):
    """User model."""

    __tablename__ = "users"

    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[list["Post"]] = relationship(back_populates="user")


class Post(Base, IdMixin):
    """Post model."""

    __tablename__ = "posts"

    title: Mapped[str]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship(back_populates="posts")
