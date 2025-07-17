from datetime import datetime
from typing import Optional, List, Any
from pydantic import (
    BaseModel, EmailStr, Field, field_validator, 
    ConfigDict, model_validator
)
from bson import ObjectId


def convert_objectid_to_str(data: Any) -> Any:
    """Recursively convert ObjectId instances to strings in a dictionary."""
    if isinstance(data, dict):
        return {k: convert_objectid_to_str(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [convert_objectid_to_str(item) for item in data]
    elif isinstance(data, ObjectId):
        return str(data)
    return data


class BaseModelWithObjectId(BaseModel):
    """Base model that automatically converts ObjectId fields to strings."""
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
    
    @model_validator(mode='before')
    @classmethod
    def convert_objectids(cls, data: Any) -> Any:
        if isinstance(data, dict):
            return convert_objectid_to_str(data)
        return data


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(BaseModelWithObjectId):
    id: str = Field(alias="_id")
    karma: int
    created_at: datetime


class PostBase(BaseModel):
    title: str
    content: str
    subreddit_id: str


class PostCreate(PostBase):
    pass


class PostResponse(BaseModelWithObjectId):
    id: str = Field(alias="_id")
    author_id: str
    votes: int
    comments: int
    created_at: datetime


class CommentCreate(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    content: str = Field(
        ...,
        min_length=1,
        description="Comment content"
    )
    post_id: str = Field(
        ...,
        pattern="^[0-9a-fA-F]{24}$",
        description="Valid MongoDB ObjectId"
    )
    parent_comment_id: str | None = Field(
        None,
        pattern="^[0-9a-fA-F]{24}$",
        description="Valid MongoDB ObjectId"
    )


class CommentResponse(BaseModelWithObjectId):
    id: str = Field(..., alias="_id")
    content: str
    author_id: str
    post_id: str
    parent_comment_id: str | None
    votes: int
    created_at: datetime = Field(..., alias="createdAt")


class VoteCreate(BaseModel):
    target_id: str
    target_type: str  # "post" or "comment"
    vote_type: int    # 1 for upvote, -1 for downvote


class SubredditCreate(BaseModel):
    name: str
    description: str
    rules: List[str] = []

    @field_validator('name')
    @classmethod
    def name_lowercase(cls, v):
        return v.lower()

    @field_validator('rules')
    @classmethod
    def rules_not_empty(cls, v):
        if not v:
            raise ValueError('Rules list cannot be empty')
        return v


class SubredditResponse(BaseModelWithObjectId):
    id: str = Field(alias="_id")
    name: str
    description: str
    rules: List[str]
    created_by: str
    moderators: List[str]
    members: int
    created_at: datetime


class TokenSchema(BaseModel):
    access_token: str
    token_type: str


class TokenDataSchema(BaseModel):
    username: Optional[str] = None
