"""Post schemas."""

from user.models import UserRead

from .models import PostRead


class PostReadWithUser(PostRead):
    """Post with user data."""

    user: UserRead
