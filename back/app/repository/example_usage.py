# Example: How to use repositories in your API routes
# This shows the "before" and "after" approach

# BEFORE (current approach in your API routes):
"""
@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db=Depends(get_db)
):
    if await db.users.find_one({
        "$or": [
            {"username": user.username},
            {"email": user.email}
        ]
    }):
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    hashed_password = get_password_hash(user.password)

    user_data = {
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "karma": 0,
        "created_at": datetime.now(UTC)
    }

    result = await db.users.insert_one(user_data)
    user_data["_id"] = result.inserted_id
    return UserResponse(**user_data)
"""

# AFTER (using repository pattern):
"""
from ..repository.user_repository import UserRepository

@router.post("/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db=Depends(get_db)
):
    user_repo = UserRepository(db)
    
    if await user_repo.username_or_email_exists(user.username, user.email):
        raise HTTPException(
            status_code=400,
            detail="Username or email already exists"
        )

    hashed_password = get_password_hash(user.password)
    user_data = await user_repo.create_user(
        user.username, 
        user.email, 
        hashed_password
    )
    
    return UserResponse(**user_data)
"""

# Benefits of the repository pattern:
# 1. Cleaner API routes - business logic separated from data access
# 2. Reusable database operations
# 3. Easier to test (you can mock repositories)
# 4. Better error handling in one place
# 5. Consistent database operations across the app 