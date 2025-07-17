from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import auth_router, users_router, posts_router, subreddits_router
from .config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup:
    yield
    # Shutdown:
    pass

app = FastAPI(title=settings.APP_NAME, lifespan=lifespan)

# Include routers
app.include_router(auth_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")
app.include_router(posts_router, prefix="/api/v1")
app.include_router(subreddits_router, prefix="/api/v1")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "Welcome to CReddit - Reddit Clone API"}
