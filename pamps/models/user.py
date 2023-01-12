"""User related data models"""
from datetime import datetime

from typing import Optional, TYPE_CHECKING
from sqlmodel import Field, SQLModel, Relationship
from pamps.security import HashedPassword
from pydantic import BaseModel

if TYPE_CHECKING:
    from pamps.models.post import Post
    from pamps.models.post import Like

class User(SQLModel, table=True):
    """Represents the User Model"""

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, nullable=False)
    username: str = Field(unique=True, nullable=False)
    avatar: Optional[str] = None
    bio: Optional[str] = None
    password: HashedPassword

    # it populates the .user attribute on the Post Model
    posts: list["Post"] = Relationship(back_populates="user")
    likes: list["Like"] = Relationship(back_populates="user")


class UserResponseBase(BaseModel):
    """Serializer for User Response"""

    id: int
    username: str


class UserResponse(UserResponseBase):
    """Serializer for User Response"""

    avatar: Optional[str] = None
    bio: Optional[str] = None


class UserRequest(BaseModel):
    """Serializer for User request payload"""

    email: str
    username: str
    password: str
    avatar: Optional[str] = None
    bio: Optional[str] = None


class Social(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    date: datetime = Field(default_factory=datetime.utcnow, nullable=False)

    from_user_id: int = Field(foreign_key="user.id")
    to_user_id: int = Field(foreign_key="user.id")

    from_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"primaryjoin": "Social.from_user_id==User.id", "lazy": "joined"}
    )
    to_user: Optional["User"] = Relationship(
        sa_relationship_kwargs={"primaryjoin": "Social.to_user_id==User.id", "lazy": "joined"}
    )


class SocialResponse(BaseModel):
    date: datetime
    from_user_id: int
    to_user_id: int


class SocialResponseWithUsers(BaseModel):
    date: datetime
    from_user: Optional[UserResponseBase] = None
    to_user: Optional[UserResponseBase] = None

class SocialRequest(BaseModel):
    date: datetime
    from_user_id: int
    to_user_id: int

