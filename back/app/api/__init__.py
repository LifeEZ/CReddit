from .auth import router as auth_router
from .users import router as users_router
from .posts import router as posts_router
from .subreddits import router as subreddits_router

# This makes imports cleaner in main.py
__all__ = ["auth_router", "users_router", "posts_router", "subreddits_router"]
