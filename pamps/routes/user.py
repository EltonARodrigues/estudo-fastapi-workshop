from typing import List

from fastapi import APIRouter
from fastapi.exceptions import HTTPException
from sqlmodel import Session, select
from pamps.auth import AuthenticatedUser

from pamps.db import ActiveSession
from pamps.models.user import (
    SocialResponseWithUsers,
    User,
    UserRequest,
    UserResponse,
    Social,
    SocialResponse
)
from pamps.models.post import (
    Post,
    PostResponseWithReplies
)

router = APIRouter() # /user


@router.get("/", response_model=List[UserResponse])
async def list_users(*, session: Session = ActiveSession):
    """List all users."""
    users = session.exec(select(User)).all()
    return users


@router.get("/{username}/", response_model=UserResponse)
async def get_user_by_username(
    *, session: Session = ActiveSession, username: str
):
    """Get user by username"""
    query = select(User).where(User.username == username)
    user = session.exec(query).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.post("/", response_model=UserResponse, status_code=201)
async def create_user(*, session: Session = ActiveSession, user: UserRequest):
    """Creates new user"""
    db_user = User.from_orm(user)  # transform UserRequest in User
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


@router.post("/follow/{id}", response_model=SocialResponse, status_code=201)
async def add_follow(*, session: Session = ActiveSession, id: int, user: User = AuthenticatedUser):
    """Follow a User"""

    if user.id == id:
        raise HTTPException(status_code=400, detail="You can't follow yourself")

    db_social = Social(from_user_id=user.id, to_user_id=id)
    session.add(db_social)
    session.commit()
    session.refresh(db_social)
    return db_social

@router.get("/{user_id}/followers", response_model=List[SocialResponseWithUsers])
def get_user_followers(*, session: Session = ActiveSession, user_id: int):
    """Get Followers of a user"""
    query = select(Social).where(Social.from_user_id == user_id)
    return session.exec(query).all()

@router.get("/user/timeline", response_model=List[PostResponseWithReplies])
def get_user_followers(*, session: Session = ActiveSession, user: User = AuthenticatedUser):
    """Get Followers of a user"""
    print(user.id)
    query = select(Post).where(Post.user_id == Social.to_user_id).where(Social.from_user_id == User.id).where(User.id == user.id)
    return session.exec(query).all()

#   .user_id = s.to_user_id and s.from_user_id = us.id and us.id = 5