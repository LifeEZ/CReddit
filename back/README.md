# Reddit Clone Backend

A FastAPI-based backend for a Reddit clone application.

## Features

- User authentication and authorization
- Post management
- Subreddit functionality
- Comment system
- MongoDB integration

## Installation

```bash
# Install dependencies
uv sync

# Run the development server
uv run python run.py
```

## Development

```bash
# Install with development dependencies
uv sync --extra dev

# Run tests
uv run pytest

# Format code
uv run black .
uv run isort .
```

## Environment Variables

Create a `.env` file with the following variables:

```env
DATABASE_URL=mongodb://localhost:27017
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
``` 