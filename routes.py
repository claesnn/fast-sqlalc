"""Define the API routes."""

from fastapi import APIRouter, HTTPException

from db import SessionDep
from post.models import PostCreate, PostRead
from post.schemas import PostReadWithUser
from services import create_post, create_user, get_post, get_user, list_posts, list_users, update_user
from user.models import UserRead, UserUpdate
from user.schemas import UserCreateWithPosts, UserReadWithPosts

router = APIRouter()


@router.post("/users", response_model=UserReadWithPosts)
def post_user(payload: UserCreateWithPosts, session: SessionDep):
    """Create a user."""
    return create_user(session, payload)


@router.get("/users/{user_id}", response_model=UserReadWithPosts)
def get_user_route(user_id: int, session: SessionDep):
    """Get a user."""
    user = get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/{user_id}/posts", response_model=PostRead)
def post_post(user_id: int, payload: PostCreate, session: SessionDep):
    """Create a post."""
    user = get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return create_post(session, payload, user_id)


@router.get("/posts/{post_id}", response_model=PostReadWithUser)
def get_post_route(post_id: int, session: SessionDep):
    """Get a post."""
    post = get_post(session, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/users", response_model=list[UserRead])
def list_users_route(session: SessionDep):
    """List users."""
    return list_users(session)


@router.get("/posts", response_model=list[PostRead])
def list_posts_route(session: SessionDep):
    """List posts."""
    return list_posts(session)


@router.patch("/users/{user_id}", response_model=UserRead)
def patch_user(user_id: int, payload: UserUpdate, session: SessionDep):
    """Update a user."""
    user = get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return update_user(session, payload, user)
