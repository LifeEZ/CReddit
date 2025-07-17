from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, UTC
from bson import ObjectId
from ..core.auth import get_current_user
from ..core.database import get_db
from ..models.schemas import PostCreate, PostResponse
from typing import List

router = APIRouter(prefix="/posts", tags=["posts"])


@router.post("/", response_model=PostResponse)
async def create_post(
    post: PostCreate,
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    # Verify subreddit exists
    if not await db.subreddits.find_one({"_id": ObjectId(post.subreddit_id)}):
        raise HTTPException(status_code=404, detail="Subreddit not found")

    post_data = {
        "title": post.title,
        "content": post.content,
        "author_id": str(current_user["_id"]),
        "subreddit_id": post.subreddit_id,
        "votes": 0,
        "comments": 0,
        "created_at": datetime.now(UTC)
    }

    result = await db.posts.insert_one(post_data)
    post_data["_id"] = result.inserted_id
    return PostResponse(**post_data)


@router.get("/", response_model=List[PostResponse])
async def list_posts(
    skip: int = 0,
    limit: int = 10,
    db=Depends(get_db)
):
    cursor = db.posts.find().skip(skip).limit(limit)
    posts = []
    async for post in cursor:
        posts.append(PostResponse(**post))
    return posts


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    db=Depends(get_db)
):
    try:
        post = await db.posts.find_one({"_id": ObjectId(post_id)})
    except (ValueError, TypeError):
        raise HTTPException(status_code=400, detail="Invalid post ID")

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return PostResponse(**post)
