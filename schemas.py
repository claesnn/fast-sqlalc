"""Schemas for the application."""

from pydantic import BaseModel, ConfigDict

from utils import partial_model


class UserBase(BaseModel):
    """Base schema for the User model."""

    name: str
    email: str


class UserCreate(UserBase):
    """Schema for creating a User."""

    posts: list["PostCreate"] = []


class UserPublic(UserBase):
    """Schema for a public User."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class UserFull(UserPublic):
    """Schema for a full User."""

    posts: list["PostPublic"]


@partial_model
class UserUpdate(UserCreate):
    """Schema for updating a User."""


class PostBase(BaseModel):
    """Base schema for the Post model."""

    title: str
    content: str


class PostCreate(PostBase):
    """Schema for creating a Post."""


class PostPublic(PostBase):
    """Schema for a public Post."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class PostFull(PostPublic):
    """Schema for a full Post."""

    user: UserPublic


@partial_model
class PostUpdate(PostBase):
    """Schema for updating a Post."""
