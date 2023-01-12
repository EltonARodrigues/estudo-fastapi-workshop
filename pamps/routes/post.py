from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select

from pamps.auth import AuthenticatedUser
from pamps.db import ActiveSession
from pamps.models.post import (
    Like,
    LikeCompleteResponde,
    Post,
    PostRequest,
    PostResponse,
    PostResponseWithReplies
)
from pamps.models.user import User

router = APIRouter()


@router.get("/", response_model=List[PostResponse])
async def list_posts(*, session: Session = ActiveSession):
    """List all posts without replies"""
    query = select(Post).where(Post.parent == None)
    posts = session.exec(query).all()
    return posts


@router.get("/{post_id}/", response_model=PostResponseWithReplies)
async def get_post_by_post_id(
    *,
    session: Session = ActiveSession,
    post_id: int,
):
    """Get post by post_id"""

    query = select(Post).where(Post.id == post_id)
    post = session.exec(query).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.get("/user/{username}/", response_model=List[PostResponse])
async def get_posts_by_username(
    *,
    session: Session = ActiveSession,
    username: str,
    include_replies: bool = False,
):
    """Get posts by username"""
    filters = [User.username == username]
    if not include_replies:
        filters.append(Post.parent == None)
    query = select(Post).join(User).where(*filters)
    posts = session.exec(query).all()
    return posts


@router.post("/", response_model=PostResponse, status_code=201)
async def create_post(
    *,
    session: Session = ActiveSession,
    user: User = AuthenticatedUser,
    post: PostRequest,
):
    """Creates new post"""

    post.user_id = user.id

    db_post = Post.from_orm(post)  # transform PostRequest in Post
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


@router.post("/{post_id}/like/", response_model=LikeCompleteResponde, status_code=201)
async def add_like_to_post(
    *,
    post_id: int,
    session: Session = ActiveSession,
    user: User = AuthenticatedUser
):
    """Add Like to a post"""

    db_like = Like(user_id=user.id, post_id=post_id)
    session.add(db_like)
    session.commit()
    session.refresh(db_like)
    return db_like


@router.get("/likes/{username}", response_model=list[PostResponse], status_code=200)
async def get_posts_with_likes(*, username: int, session: Session = ActiveSession):
    """Posts liked by user"""

    query = select(Post).where(Post.id == Like.post_id).where(Like.user_id==username)
    posts = session.exec(query).all()
    return posts