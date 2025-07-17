from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime, UTC
from ..core.auth import get_current_user
from ..core.database import get_db
from ..models.schemas import SubredditCreate, SubredditResponse
from typing import List

router = APIRouter(prefix="/subreddits", tags=["subreddits"])


@router.post("/", response_model=SubredditResponse)
async def create_subreddit(
    subreddit: SubredditCreate,
    current_user=Depends(get_current_user),
    db=Depends(get_db)
):
    if await db.subreddits.find_one({"name": subreddit.name}):
        raise HTTPException(
            status_code=400,
            detail="Subreddit name already exists"
        )

    subreddit_data = {
        "name": subreddit.name,
        "description": subreddit.description,
        "rules": subreddit.rules,
        "created_by": str(current_user["_id"]),
        "moderators": [str(current_user["_id"])],
        "members": 1,
        "created_at": datetime.now(UTC)
    }

    result = await db.subreddits.insert_one(subreddit_data)
    subreddit_data["_id"] = result.inserted_id
    return SubredditResponse(**subreddit_data)


@router.get("/", response_model=List[SubredditResponse])
async def list_subreddits(
    skip: int = 0,
    limit: int = 10,
    db=Depends(get_db)
):
    cursor = db.subreddits.find().skip(skip).limit(limit)
    subreddits = []
    async for subreddit in cursor:
        subreddits.append(SubredditResponse(**subreddit))
    return subreddits


@router.get("/{subreddit_name}", response_model=SubredditResponse)
async def get_subreddit(
    subreddit_name: str,
    db=Depends(get_db)
):
    subreddit = await db.subreddits.find_one({"name": subreddit_name})
    if not subreddit:
        raise HTTPException(status_code=404, detail="Subreddit not found")

    return SubredditResponse(**subreddit)
