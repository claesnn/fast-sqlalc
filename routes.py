"""Define the API routes."""

from fastapi import APIRouter, HTTPException

from db import SessionDep
from schemas import PostCreate, PostFull, PostPublic, UserCreate, UserFull, UserPublic
from services import create_post, create_user, get_post, get_user, list_posts, list_users

router = APIRouter()


@router.post("/users", response_model=UserPublic)
def post_user(payload: UserCreate, session: SessionDep):
    """Create a user."""
    return create_user(session, payload)


@router.get("/users/{user_id}", response_model=UserFull)
def get_user_route(user_id: int, session: SessionDep):
    """Get a user."""
    user = get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/users/{user_id}/posts", response_model=PostPublic)
def post_post(user_id: int, payload: PostCreate, session: SessionDep):
    """Create a post."""
    user = get_user(session, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return create_post(session, payload, user_id)


@router.get("/posts/{post_id}", response_model=PostPublic)
def get_post_route(post_id: int, session: SessionDep):
    """Get a post."""
    post = get_post(session, post_id)
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/users", response_model=list[UserPublic])
def list_users_route(session: SessionDep):
    """List users."""
    return list_users(session)


@router.get("/posts", response_model=list[PostPublic])
def list_posts_route(session: SessionDep):
    """List posts."""
    return list_posts(session)