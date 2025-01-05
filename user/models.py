"""Models and schemas for user management."""

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from utils import partial_model

if TYPE_CHECKING:
    from post.models import Post


class User(Base):
    """User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="user")


class UserBase(BaseModel):
    """Base schema for the User model."""

    name: str
    email: str


class UserCreate(UserBase):
    """Schema for creating a User."""


class UserRead(UserBase):
    """Schema for a public User."""

    model_config = ConfigDict(from_attributes=True)

    id: int


@partial_model
class UserUpdate(UserCreate):
    """Schema for updating a User."""
