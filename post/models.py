"""Models and schemas for the posts."""

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base
from utils import partial_model

if TYPE_CHECKING:
    from user.models import User


class Post(Base):
    """Post model."""

    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str]
    content: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    user: Mapped["User"] = relationship("User", back_populates="posts")


class PostBase(BaseModel):
    """Base schema for the Post model."""

    title: str
    content: str


class PostCreate(PostBase):
    """Schema for creating a Post."""


class PostRead(PostBase):
    """Schema for a public Post."""

    model_config = ConfigDict(from_attributes=True)

    id: int


@partial_model
class PostUpdate(PostBase):
    """Schema for updating a Post."""
